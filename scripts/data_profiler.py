#!/usr/bin/env python3
"""
Data Profiler — 为 /climpub data to idea 命令服务
读取 CSV/XLSX，输出结构化数据画像：变量字典、分布摘要、缺失模式、相关性、研究类型预判

Usage:
    python data_profiler.py data.csv
    python data_profiler.py data.xlsx --sheet Sheet1
    python data_profiler.py data.csv --output profile.json
"""

import sys
import json
import argparse
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print('{"error": "pandas is required. Install: pip install pandas openpyxl"}')
    sys.exit(1)


# ---------- 变量名称模式 ----------
OUTCOME_PATTERNS = [
    "outcome", "结局", "diagnosis", "diagnose", "status", "death", "dead",
    "event", "survival", "mortality", "survive", "结局", "预后", "生存",
    "response", "remission", "复发", "recurrence", "progression", "恶化",
]

EXPOSURE_PATTERNS = [
    "group", "treatment", "arm", "exposure", "暴露", "分组", "干预",
    "trt", "randomization", "rand", "随机", "疗法", "therapy",
]

TIME_PATTERNS = [
    "time", "follow", "follow_up", "followup", "survival_time",
    "months", "days", "years", "随访", "时间", "生存时间",
    "duration", "length", "period",
]

COVARIATE_PATTERNS = [
    "age", "年龄", "sex", "gender", "性别", "bmi", "education", "教育",
    "smoke", "smoking", "吸烟", "drink", "alcohol", "饮酒", "饮酒",
    "race", "ethnicity", "种族",
]

BIOMARKER_PATTERNS = [
    "biomarker", "标志物", "标记", "protein", "蛋白", "gene", "基因",
    "level", "浓度", "serum", "血浆", "plasma", "csf", "脑脊液",
    "score", "评分", "scale", "量表",
]

MATCH_PATTERNS = [
    "match", "matching", "匹配", "pair", "配对", "id", "patient_id",
    "subject_id",
]

ID_PATTERNS = [
    "id", "patient_id", "subject_id", "participant_id", "序号",
]


def detect_variable_role(name: str) -> str:
    """根据变量名推断角色"""
    name_lower = name.lower().replace("_", "").replace("-", "")

    # ID 变量
    if any(p in name_lower for p in ID_PATTERNS):
        return "id"

    # 结局变量优先匹配
    if any(p in name_lower for p in OUTCOME_PATTERNS):
        return "outcome"

    # 暴露/分组变量
    if any(p in name_lower for p in EXPOSURE_PATTERNS):
        return "exposure"

    # 时间变量
    if any(p in name_lower for p in TIME_PATTERNS):
        return "time"

    # 标志物
    if any(p in name_lower for p in BIOMARKER_PATTERNS):
        return "biomarker"

    # 协变量
    if any(p in name_lower for p in COVARIATE_PATTERNS):
        return "covariate"

    # 匹配变量
    if any(p in name_lower for p in MATCH_PATTERNS):
        return "matching"

    return "unknown"


def infer_study_type(profile: Dict[str, Any]) -> Dict[str, Any]:
    """根据数据特征推断研究设计类型"""
    variables = profile.get("variables", [])
    roles = [v["role"] for v in variables]

    has_outcome = "outcome" in roles
    has_exposure = "exposure" in roles
    has_time = "time" in roles
    has_matching = "matching" in roles

    # 统计各角色数量
    biomarker_count = roles.count("biomarker")

    # 检查是否有 RCT 分组
    has_rct_group = False
    for v in variables:
        if v["role"] == "exposure":
            name_lower = v["name"].lower()
            if any(p in name_lower for p in ["randomization", "rand", "随机"]):
                has_rct_group = True

    # 检查是否有时间+事件（生存分析信号）
    has_event = False
    for v in variables:
        name_lower = v["name"].lower()
        if any(p in name_lower for p in ["event", "death", "dead", "status", "结局", "死亡"]):
            has_event = True

    suggestions = []

    if has_rct_group and has_outcome:
        suggestions.append({
            "type": "RCT",
            "confidence": "high",
            "reason": "检测到随机分组标识和结局变量",
            "methods": ["基线表", "组间比较", "回归分析"],
        })

    if has_time and has_event:
        # 时间+事件-存在生存数据
        if has_exposure:
            suggestions.append({
                "type": "队列研究 (Cohort)",
                "confidence": "high",
                "reason": "检测到时间-事件数据+暴露分组",
                "methods": ["KM 生存曲线", "Cox 回归", "亚组分析", "敏感性分析"],
            })

    if has_exposure and has_outcome and not has_time:
        suggestions.append({
            "type": "横断面研究 (Cross-sectional)",
            "confidence": "medium",
            "reason": "有暴露和结局变量但无时间维度",
            "methods": ["Logistic 回归", "基线表", "亚组分析"],
        })

    if has_matching and has_outcome:
        suggestions.append({
            "type": "病例对照研究 (Case-Control)",
            "confidence": "medium",
            "reason": "检测到匹配标识和结局变量",
            "methods": ["条件 Logistic 回归", "ROC 分析", "亚组分析"],
        })

    if biomarker_count >= 3:
        suggestions.append({
            "type": "标志物面板研究 (Biomarker Panel)",
            "confidence": "high" if has_outcome else "medium",
            "reason": f"检测到 {biomarker_count} 个标志物变量",
            "methods": ["LASSO 特征选择", "ROC 分析", "多标志物联合诊断"],
        })

    if biomarker_count >= 1 and has_outcome:
        suggestions.append({
            "type": "诊断性研究 (Diagnostic)",
            "confidence": "high",
            "reason": "有标志物和结局变量",
            "methods": ["ROC 曲线", "敏感度/特异度", "最佳阈值"],
        })

    # 如果什么都没匹配到，给描述性
    if not suggestions:
        suggestions.append({
            "type": "描述性研究 (Descriptive)",
            "confidence": "high",
            "reason": "未检测到明确的分组或结局变量",
            "methods": ["人口学特征描述", "临床特征分布", "共病模式"],
        })

    return {
        "suggestions": suggestions,
        "has_outcome": has_outcome,
        "has_exposure": has_exposure,
        "has_time": has_time,
        "biomarker_count": biomarker_count,
        "n_variables": len(variables),
    }


def profile_data(filepath: str, sheet: Optional[str] = None) -> Dict[str, Any]:
    """对数据文件进行完整画像"""
    ext = Path(filepath).suffix.lower()

    # 读取数据
    if ext == ".csv":
        df = pd.read_csv(filepath, low_memory=False)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(filepath, sheet_name=sheet if sheet is not None else 0)
    else:
        return {"error": f"Unsupported format: {ext}"}

    profile = {
        "file": os.path.basename(filepath),
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "column_names": list(df.columns),
        "variables": [],
        "missing_summary": {},
        "correlation_warning": False,
    }

    # 逐变量分析
    for col in df.columns:
        var_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "n_unique": int(df[col].nunique()),
            "n_missing": int(df[col].isna().sum()),
            "missing_pct": round(float(df[col].isna().mean() * 100), 1),
        }

        # 推断角色
        var_info["role"] = detect_variable_role(col)

        # 根据数据类型和取值推断类型
        if pd.api.types.is_numeric_dtype(df[col]):
            non_null = df[col].dropna()
            if len(non_null) > 0:
                var_info["type"] = "continuous"
                var_info["min"] = round(float(non_null.min()), 4)
                var_info["max"] = round(float(non_null.max()), 4)
                var_info["mean"] = round(float(non_null.mean()), 4)
                var_info["median"] = round(float(non_null.median()), 4)
                var_info["std"] = round(float(non_null.std()), 4)
                var_info["q1"] = round(float(non_null.quantile(0.25)), 4)
                var_info["q3"] = round(float(non_null.quantile(0.75)), 4)
                # 检查是否为整数编码的分类变量
                unique_vals = non_null.unique()
                if len(unique_vals) <= 5 and len(unique_vals) < len(non_null) * 0.1:
                    var_info["type"] = "categorical_encoded"
                    var_info["unique_values"] = sorted([int(x) if x == x else x for x in unique_vals])
            else:
                var_info["type"] = "empty"
        else:
            var_info["type"] = "categorical"
            value_counts = df[col].value_counts(normalize=True).head(10)
            var_info["top_values"] = [
                {"value": str(k), "pct": round(float(v * 100), 1)}
                for k, v in value_counts.items()
            ]

        profile["variables"].append(var_info)

    # 缺失总结
    missing_vars = [
        {"name": v["name"], "missing_pct": v["missing_pct"]}
        for v in profile["variables"]
        if v["missing_pct"] > 0
    ]
    missing_vars.sort(key=lambda x: x["missing_pct"], reverse=True)
    profile["missing_summary"] = {
        "total_vars_with_missing": len(missing_vars),
        "high_missing_vars": [v for v in missing_vars if v["missing_pct"] > 20],
        "medium_missing_vars": [v for v in missing_vars if 5 <= v["missing_pct"] <= 20],
        "low_missing_vars": [v for v in missing_vars if v["missing_pct"] < 5],
    }

    # 相关性矩阵（数值变量超过 30 个时只做警告）
    numeric_cols = [v["name"] for v in profile["variables"]
                    if v.get("type") in ("continuous", "categorical_encoded")]
    if len(numeric_cols) > 30:
        profile["correlation_warning"] = "数值变量超过 30 个，跳过完整相关性矩阵"
    elif len(numeric_cols) >= 2:
        corr_df = df[numeric_cols].corr(method="spearman")
        high_corr = []
        for i in range(len(corr_df.columns)):
            for j in range(i + 1, len(corr_df.columns)):
                val = corr_df.iloc[i, j]
                if abs(val) > 0.8:
                    high_corr.append({
                        "var1": corr_df.columns[i],
                        "var2": corr_df.columns[j],
                        "correlation": round(float(val), 3),
                    })
        profile["high_correlations"] = high_corr[:20]  # 最多 20 条
    else:
        profile["high_correlations"] = []

    # 研究类型预判
    profile["study_type"] = infer_study_type(profile)

    # 角色汇总
    role_summary = {}
    for v in profile["variables"]:
        role = v["role"]
        if role not in role_summary:
            role_summary[role] = []
        role_summary[role].append(v["name"])
    profile["role_summary"] = role_summary

    # 样本量评估
    n = profile["n_rows"]
    if n < 50:
        profile["sample_size_assessment"] = "非常小（<50），仅适合描述性研究"
    elif n < 200:
        profile["sample_size_assessment"] = "偏小（50-200），适合简单比较或描述性研究"
    elif n < 500:
        profile["sample_size_assessment"] = "中等（200-500），可做回归分析"
    elif n < 2000:
        profile["sample_size_assessment"] = "较大（500-2000），适合多数分析方法"
    else:
        profile["sample_size_assessment"] = "大样本（>2000），可支持复杂建模和亚组分析"

    return profile


def main():
    parser = argparse.ArgumentParser(description="Data Profiler for /climpub data to idea")
    parser.add_argument("filepath", help="CSV 或 XLSX 文件路径")
    parser.add_argument("--sheet", help="Excel 工作表名（xlsx 时使用）")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(json.dumps({"error": f"文件不存在: {args.filepath}"}))
        sys.exit(1)

    profile = profile_data(args.filepath, args.sheet)

    output = json.dumps(profile, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Profile saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
