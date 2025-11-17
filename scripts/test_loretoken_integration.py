#!/usr/bin/env python3
"""
Test full LoreToken integration in SAIQL-Delta
"""

import os
import sys
from pathlib import Path

SAIQL_HOME = Path(os.environ.get('SAIQL_HOME', Path.home() / 'SAIQL.DELTA'))
sys.path.insert(0, str(SAIQL_HOME))

try:
    from saiql_delta.core import (
        SymbolicLoreToken,
        SymbolicLoreTokenEngine,
        LoreTokenTranslator,
    )
    from saiql_delta.core.hybrid_loretoken_engine import HybridLoreToken
except ModuleNotFoundError as exc:
    raise SystemExit(
        "saiql_delta not found. Set SAIQL_HOME or install the SAIQL Delta package before running this test."
    ) from exc

def test_loretoken_integration():
    print("Testing Full LoreToken Integration")
    print("=" * 50)
    # (rest of file unchanged...)

if __name__ == "__main__":
    test_loretoken_integration()
