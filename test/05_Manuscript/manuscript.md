---
generated_by: scripts/assemble_manuscript.py
generated_at: 2026-10-18
word_count: 4008
title: "真实临床样本中治疗状态与症状负担的横断面关联：基于基线可比性的探索性分析"
---

<!-- 本文件是生成物，请勿手改。
     要修改内容，请编辑 05_Manuscript/sections/*.md 后重新运行：
       python scripts/assemble_manuscript.py
-->

# 真实临床样本中治疗状态与症状负担的横断面关联：基于基线可比性的探索性分析

## Abstract

**背景**　症状负担是影响患者生活质量的核心临床问题。随机对照试验支持治疗的有效性，但真实临床环境中接受治疗者与未接受者往往在基线即不可比，导致观察性比较易受适应证混杂影响。本研究检验在剔除可测混杂后，治疗状态与症状负担的关联是否依然存在。

**方法**　横断面研究，纳入 102 例具有完整关键变量的成年患者（对照组 48 例，治疗组 54 例）。主要结局为治疗后的症状评分（0–100，分值越高症状越重）；该结局系在比较四个候选指标的组间差异后确定，属事后选择。组间差异以 Welch t 检验估计，并以多重线性回归调整年龄、性别与体质指数。稳健性通过 Wilcoxon 秩和检验与多重插补（m = 20）评估。所有推断按探索性结果解释，未作多重比较校正。

**结果**　治疗前症状评分在两组间高度一致（49.6 vs 50.1，标准化均数差 0.04）。调整年龄、性别与体质指数后，治疗组的治疗后症状评分较对照组低 9.01 分（95% CI −15.47 至 −2.55；P = 0.00678；Cohen's d = −0.56）。年龄、性别与体质指数均与结局无统计学关联。四种分析路径（未调整、调整、Wilcoxon 秩和、多重插补）的估计介于 −9.01 至 −10.48 分之间，95% 置信区间均未跨越零。

**结论**　在该横断面样本中，治疗状态与更低的症状负担相关，且该关联无法由人口学特征、体型构成或基线严重度解释。受横断面设计与结局事后确定的限制，这一发现应作为待验证的假设，而非治疗有效的证据。

## Introduction

症状负担是这类患者最直接影响生活质量的临床问题之一。症状评分的轻微变化，往往对应着睡眠、日常活动能力与照护负担的实质差别。[1,2]正因如此，临床医生在为具体患者决定是否启动治疗时，最想知道的不是"平均而言治疗有效吗"，而是"像我面前这位患者一样的人，治疗后会更好吗"。这个问题的答案取决于两个前提：治疗确实改变了症状轨迹，以及接受治疗者与未接受治疗者本来是可以比较的。

随机对照试验为第一个前提提供了最好的证据。但随机试验的人群经过严格筛选，合并症少、依从性高，与真实临床环境中的患者存在系统性差异。[3]在真实世界中，是否接受治疗本身就是一个复杂的决策结果——症状更重的人更可能被治疗，而症状更重恰恰预示着更差的结局。这种"适应证混杂"使得直接比较治疗组与未治疗组的观察性研究极易得出偏倚的方向。[4,5]因此，真实世界数据能否在**剔除可测混杂之后**仍然显示组间差异，是判断观察性证据价值的关键一步。

本研究利用一份横断面临床样本回答这一问题。我们首先检验两组在治疗前的症状严重程度上是否可比，以此为后续比较提供可验证的均衡性证据；随后在调整年龄、性别与体质指数后估计组间差异；最后通过非参数检验与多重插补检验结论的稳健性。我们的先验假设是：若治疗状态与更低的症状负担相关，那么这一差异应当在治疗前评分可比的前提下依然存在，并且不应随缺失处理方式或分布假设而改变。需要指出的是，本研究的结局指标系在比较候选指标后确定，全部推断均按探索性结果处理。

## Methods

### 研究设计与研究对象

本研究为横断面研究，纳入 120 例连续就诊的成年患者。纳入标准为年龄 ≥ 18 岁且关键临床变量可获得；排除标准为症状评分缺失或分组信息不可追溯。

研究方案经机构伦理委员会批准（批号 TEST-IRB-2026-001）。鉴于本研究仅使用去标识化的既有数据，伦理委员会豁免了个体知情同意的签署要求。

最终分析样本为 102 例（对照组 48 例，治疗组 54 例）。18 例（15.0%）因病历中 `bmi`、治疗前症状评分或肾功能的缺失而被排除。研究按 STROBE 声明的条目组织报告。[6]

### 变量与测量

**分组变量**：`group` 将患者分为对照组与治疗组，依据其实际接受的治疗状态划分。在横断面设计下，该变量用于组间比较，不用于估计干预效应。

**结局变量**：治疗后的症状评分为连续变量，取值 0–100，分值越高表示症状越重。本研究的结局指标在分析过程中确定，属事后（post hoc）选择，具体说明见「统计分析」小节。

**协变量**：年龄（岁）、性别与体质指数（kg/m²）。三者均在建模前预先设定，不依据单因素检验结果筛选。

**其他变量**：肾功能以估算肾小球滤过率（mL/min/1.73 m²）表示；共病状态分为无共病、高血压、糖尿病及两者并存四类。

### 统计分析

连续变量以均数（标准差）描述，分类变量以频数（百分比）描述。组间比较：连续变量采用 Welch t 检验，分类变量采用 Pearson χ² 检验，效应量分别以标准化均数差与 Cramér's V 表示。连续变量间的关联以 Pearson 相关系数评估。

主分析采用多重线性回归模型，以治疗后症状评分为因变量，纳入分组、年龄、性别与体质指数，报告回归系数、95% 置信区间与精确 P 值。模型诊断包括残差正态性（Shapiro-Wilk 检验）、方差膨胀因子与 Cook's 距离；Cook's 距离超过 4/n 的观测予以保留，不作剔除。

稳健性通过三条独立路径评估：（1）未调整的组间比较；（2）Wilcoxon 秩和检验，不依赖正态性假设；（3）多重插补（链式方程，m = 20，固定随机种子），插补模型纳入结局、分组、年龄、性别、体质指数与共病状态，并按 Rubin 规则汇总。[7,8]所有方法的效应方向统一为「治疗组减对照组」。

数据分析使用 R 4.4.3 完成，主要依赖 ggplot2、dplyr、tidyr、patchwork 与 mice 扩展包。双侧 P < 0.05 视为具有统计学意义。**由于主要结局系在观察各候选指标的组间差异后确定，本研究未作多重比较校正，所有 P 值与置信区间均应按探索性解释，不具确证性。**

### 分析决策的透明性声明

本研究未预设主要结局。分析按迭代方式推进：首批完成基线描述与四个候选指标的组间筛查，据此确定主要结局；第二批完成调整模型与稳健性分析。全部决策、依据与被否决的备选方案记录于分析日志（`.clinpub/ANALYSIS_LOG.md`），供读者核对。

未被采纳的分析包括：按年龄、性别或共病状态的分层分析（样本量不足以支撑分层后的检验效能）、限制性立方样条（缺乏非线性关系的先验依据）以及共病与分组的交互项检验（四分类与二分类交叉后各组样本过少）。上述未做分析对本研究解释范围的限制，在讨论部分的局限性中说明。

## Results

### 样本与基线特征

研究共纳入 120 例患者，其中 18 例（15.0%）因关键变量缺失被排除，最终分析样本为 102 例（对照组 48 例，治疗组 54 例）。两组在年龄（56.0 岁 vs 58.1 岁；P = 0.347）、体质指数（23.8 vs 24.3 kg/m²；P = 0.432）、性别构成（女性 58.3% vs 55.6%；P = 0.934）及共病分布（P = 0.216）方面均未见统计学差异（Table 1）。治疗前症状评分在两组间高度一致（49.6 vs 50.1；标准化均数差 0.04），肾功能亦相近（89.8 vs 93.1 mL/min/1.73 m²；P = 0.255）。

### 候选结局指标的组间比较

在四个候选结局指标中，仅治疗后的症状评分表现出组间差异（Figure 1）。治疗组 `post_score` 均值为 37.54，对照组为 46.65，差值 −9.11（95% CI −15.46 至 −2.75；Cohen's d = −0.56；P = 0.00541）。治疗前症状评分的组间差值为 0.54（95% CI −4.80 至 5.88；d = 0.04；P = 0.840），肾功能的组间差值为 3.31（95% CI −2.43 至 9.04；d = 0.23；P = 0.255）。共病分布与分组无关（Cramér's V = 0.209；P = 0.216）。三个连续指标均近似正态分布（Shapiro-Wilk P 分别为 0.172、0.379 与 0.632）。

相关性分析显示，治疗前与治疗后症状评分的 Pearson 相关系数为 r = 0.84（Figure 1）。肾功能与其余四个连续指标的相关性绝对值均不超过 0.12。

### 主分析：调整后的组间差异

以治疗后症状评分为结局的多重线性回归显示，调整年龄、性别与体质指数后，治疗组较对照组的评分低 9.01 分（95% CI −15.47 至 −2.55；P = 0.00678）（Table 2、Figure 2）。未调整模型的结果为 −9.11 分（95% CI −15.52 至 −2.70；P = 0.00578）。年龄（每增加 1 岁：0.12 分，95% CI −0.19 至 0.42；P = 0.440）、性别（男性 vs 女性：1.76 分，95% CI −4.89 至 8.41；P = 0.601）与体质指数（每增加 1 kg/m²：−0.69 分，95% CI −1.62 至 0.23；P = 0.141）均与结局无统计学关联。标准化回归系数分别为 −0.28（分组）、0.09（年龄）、0.05（性别）与 −0.15（体质指数）。

模型诊断显示残差近似正态（Shapiro-Wilk P = 0.164），方差膨胀因子介于 1.03 与 1.11 之间，Cook's 距离超过 4/n 阈值的观测共 4 例，均予保留。

### 稳健性分析

四种分析路径给出的组间差异方向和量级一致（Figure 3）：未调整模型 −9.11（95% CI −15.52 至 −2.70；P = 0.00578），调整模型 −9.01（95% CI −15.47 至 −2.55；P = 0.00678），Wilcoxon 秩和检验 −10.00（95% CI −16.00 至 −3.00；P = 0.00372），多重插补后（n = 120，m = 20）−10.48（95% CI −16.40 至 −4.56；P = 0.000654）。四种方法的 95% 置信区间均未跨越零。完整病例分析与多重插补分析之间的点估计差异为 1.47 分，小于任一置信区间的宽度。

## Discussion

### 主要发现

在接受治疗的临床样本中，治疗组治疗后的症状评分较对照组低约 9 分（0–100 量表），效应量为中等。该差异在调整年龄、性别与体质指数后基本不变，并在非参数检验与多重插补两条独立路径下保持一致。治疗前症状评分在两组间几乎完全一致，肾功能与分组无关。综合来看，组间差异既不能由人口学与体型构成解释，也不能由基线严重度或肾功能差异解释。

### 与既往研究的比较与解释

本研究的效应量（标准化均数差约 0.56）落在同类干预研究报告的中等效应区间内。[9,10,11]与多数随机对照试验不同，本研究的分组并非随机分配，因此观察到的差异同时包含了治疗本身的作用与选择治疗的因素。治疗前评分的组间平衡（标准化均数差 0.04）在一定程度上缓解了这一担忧：如果分组主要取决于基线严重度，那么治疗前评分本应出现系统性差异。然而基线平衡也可能源于样本量有限下的偶然，不能等同随机化。

从机制上看，症状评分的改善可能通过症状负荷的减轻而非器官功能的改变实现——本研究中肾功能与分组及结局均无关联，提示所观察到的变化并不以肾功能改善为中介。[12]这一推断与本研究的设计相称，但缺乏直接的机制测量，应视为有待验证的假设。

临床上，约 9 分的降幅接近该量表的最小临床重要差异量级，意味着差异不只是统计学显著，也可能具有患者可感知的意义。但横断面设计无法回答「治疗是否导致了改善」，因此这一解读只能作为假设提出。

### 局限性

第一，**横断面设计**限制了因果推断。分组反映的是治疗状态而非随机分配的干预，观察到的差异可能由未测量的适应证混杂（confounding by indication）造成。本研究调整的协变量仅为年龄、性别与体质指数，未涵盖疾病病程、合并用药与社会经济状况。

第二，**主要结局系事后确定**。研究未预设结局，而是在比较四个候选指标的组间差异后选定症状评分。这一过程使 P 值与置信区间带有选择效应，未经多重比较校正，也不具备确证性。文中所有统计推断均应视为探索性结果，需在前瞻性研究中重复。

第三，**样本量有限**（N = 102）。这直接导致若干分析无法开展：按年龄、性别或共病状态的分层分析在分层后每组仅约 20–30 例，检验效能不足；共病四分类与分组交叉后的交互检验各组样本过少；以限制性立方样条考察非线性关系缺乏先验依据且样本不足以稳定拟合。这三类分析均被主动放弃，其结果是本研究无法判断效应是否在特定亚组中更强，也无法排除阈值型或 U 型关系。

第四，**缺失数据处理依赖假设**。完整病例分析隐含完全随机缺失假设，多重插补隐含随机缺失假设。18 例被排除者的缺失比例在变量间相对均衡，但缺失机制本身未被验证；若缺失与未观测的症状严重度相关，两种方法都可能产生偏倚。此外，插补模型未纳入治疗前症状评分，而后者与结局高度相关（r = 0.84），这可能降低插补效率。

第五，**共病未作有序编码**。本研究将共病状态作为四分类变量处理，因而无法检验「共病负担越重、症状评分越高」这一梯度假设。若该梯度存在，四分类模型会将其稀释为若干不显著的组间对比。

第六，**4 例强影响观测未剔除**。这些观测的 Cook's 距离超过 4/n 阈值，但既无录入错误证据，也无生理学越界，故予保留。保留避免了选择性偏倚，但也意味着主分析的估计对这些点具有一定敏感性。

第七，**单一中心与单一时点**。数据来自单一时点的横断面采集，无法反映症状随时间的变化轨迹，也无法评估治疗持续时间的影响。

### 结论

在这一横断面样本中，接受治疗者的症状评分低于未接受治疗者，差异在调整可测混杂后依然存在，并对缺失处理与分布假设稳健。由于设计限制与结局的事后确定，这一发现应作为待验证的假设，而非治疗有效的证据；其临床意义需要在具备随机分配与纵向随访的研究中确认。

## Conclusion

在这一横断面样本中，接受治疗者的症状负担低于未接受治疗者，且该关联无法由年龄、性别、体型构成或基线严重度解释。这一发现提示治疗状态可能与症状改善相关，但受设计所限，它只是一个值得在前瞻性研究中检验的假设，尚不足以支持治疗决策。

## References

1. Vyas C, Donneyong M, Mischoulon D, Chang G, Gibson H, Cook N, et al. Association of Race and Ethnicity With Late-Life Depression Severity, Symptom Burden, and Care. JAMA network open. 2020. doi:10.1001/jamanetworkopen.2020.1606

2. Triolo F, Vetrano D, Trevisan C, Sjöberg L, Calderón-Larrañaga A, Belvederi Murri M, et al. Mapping 15-year depressive symptom transitions in late life: population-based cohort study. The British journal of psychiatry : the journal of mental science. 2024. doi:10.1192/bjp.2024.84

3. Steffens D, Diniz B, Jain N, Kluewer-D'Amico J, Manning K, Wang L. Moderators of treatment response in late-life depression. Neuropsychopharmacology : official publication of the American College of Neuropsychopharmacology. 2026. doi:10.1038/s41386-026-02337-x

4. Lee J, Chang S. Confounding by Indication in Studies of Selective Serotonin Reuptake Inhibitors. Psychiatry investigation. 2022. doi:10.30773/pi.2022.0209

5. Remschmidt C, Wichmann O, Harder T. Frequency and impact of confounding by indication and healthy vaccinee bias in observational studies assessing influenza vaccine effectiveness: a systematic review. BMC infectious diseases. 2015. doi:10.1186/s12879-015-1154-y

6. von Elm E, Altman D, Egger M, Pocock S, Gøtzsche P, Vandenbroucke J, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Journal of clinical epidemiology. 2008. doi:10.1016/j.jclinepi.2007.11.008

7. Allotey P, Harel O. Multiple Imputation for Incomplete Data in Environmental Epidemiology Research. Current environmental health reports. 2019. doi:10.1007/s40572-019-00230-y

8. Wijesuriya R, Moreno-Betancur M, Carlin J, White I, Quartagno M, Lee K. Multiple Imputation for Longitudinal Data: A Tutorial. Statistics in medicine. 2025. doi:10.1002/sim.10274

9. Tunvirachaisakul C, Gould R, Coulson M, Ward E, Reynolds G, Gathercole R, et al. Predictors of treatment outcome in depression in later life: A systematic review and meta-analysis. Journal of affective disorders. 2018. doi:10.1016/j.jad.2017.10.008

10. Göke K, Trevizol A, Ma C, Mah L, Rajji T, Daskalakis Z, et al. Predictors of remission after repetitive transcranial magnetic stimulation for the treatment of late-life depression. Psychiatry research. 2024. doi:10.1016/j.psychres.2024.115822

11. Joel I, Begley A, Mulsant B, Lenze E, Mazumdar S, Dew M, et al. Dynamic prediction of treatment response in late-life depression. The American journal of geriatric psychiatry : official journal of the American Association for Geriatric Psychiatry. 2014. doi:10.1016/j.jagp.2012.07.002

12. Hou Z, Ming Y, Lu K, Ma Y, Jia R, Lai G, et al. Cumulative and variable depression symptom exposure and incident dementia: Panel data analysis of four longitudinal cohort studies. Alzheimer's & dementia : the journal of the Alzheimer's Association. 2025. doi:10.1002/alz.70950
