#!/usr/bin/env python3
"""
Shared NCBI E-Utilities client module.

Provides session management, rate limiting, API key handling, and shared constants
used by both ncbi_search.py and pubmed_search.py.

Usage:
    from ncbi_client import create_session, get_api_key, rate_limit, GENE_SYMBOLS
"""

import os
import sys
import time
import argparse
from typing import Optional

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

# NCBI E-Utilities Base URLs
EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ESEARCH_URL = f"{EUTILS_BASE}/esearch.fcgi"
ESUMMARY_URL = f"{EUTILS_BASE}/esummary.fcgi"
EFETCH_URL = f"{EUTILS_BASE}/efetch.fcgi"
ELINK_URL = f"{EUTILS_BASE}/elink.fcgi"

# Known gene symbols used by both ncbi_search and pubmed_search
GENE_SYMBOLS = [
    "APOE", "APP", "PSEN1", "PSEN2", "TREM2", "MAPT", "SNCA", "TARDBP",
    "BRCA1", "BRCA2", "TP53", "EGFR", "KRAS", "MYC", "PTEN", "VEGF",
    "IL6", "TNF", "IFNG", "IL1B", "IL10", "TGFB1",
    "BDNF", "NGF", "GDNF", "NTF3",
]

# Rate limiting — NCBI enforces 3 req/s without API key, 10 req/s with API key
# https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.How_to_Make_Requests
LAST_REQUEST_TIME = 0
NCBI_NO_KEY_INTERVAL = 0.34   # ~3 req/s
NCBI_KEY_INTERVAL = 0.11      # ~9 req/s (built-in safety margin below 10)
SESSION = None


def create_session():
    """Create a requests Session with retry logic for NCBI E-Utilities."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_api_key(args: argparse.Namespace) -> Optional[str]:
    """Get NCBI API key from command-line args or NCBI_API_KEY environment variable."""
    if args.api_key:
        return args.api_key
    return os.environ.get("NCBI_API_KEY")


def rate_limit(api_key: Optional[str]):
    """Enforce NCBI E-Utilities rate limit (3 req/s without key, ~9 req/s with key)."""
    global LAST_REQUEST_TIME
    interval = NCBI_KEY_INTERVAL if api_key else NCBI_NO_KEY_INTERVAL
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < interval:
        time.sleep(interval - elapsed)
    LAST_REQUEST_TIME = time.time()


def print_api_key_tip():
    """Print a tip about setting NCBI_API_KEY when not configured."""
    print("=" * 60, file=sys.stderr)
    print("Tip: NCBI_API_KEY 未设置。", file=sys.stderr)
    print("", file=sys.stderr)
    print("  无 key 仍可检索，但限速  3 次/秒。", file=sys.stderr)
    print("  设置 API key 后可提速至 10 次/秒。", file=sys.stderr)
    print("", file=sys.stderr)
    print("  申请地址: https://ncbi.nlm.nih.gov/account/settings/", file=sys.stderr)
    print("", file=sys.stderr)
    print("  方式一 — 临时设置 (当前终端会话):", file=sys.stderr)
    print("    export NCBI_API_KEY=your_key_here", file=sys.stderr)
    print("", file=sys.stderr)
    print("  方式二 — 持久设置 (推荐，所有项目可用):", file=sys.stderr)
    print("    将 export NCBI_API_KEY=your_key_here 添加到 ~/.bashrc", file=sys.stderr)
    print("", file=sys.stderr)
    print("  方式三 — 项目级设置:", file=sys.stderr)
    print("    echo 'NCBI_API_KEY=your_key_here' >> .env", file=sys.stderr)
    print("    (.env 已在 .gitignore 中，不会提交)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
