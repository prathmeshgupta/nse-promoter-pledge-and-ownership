"""Quality and Integrity Audit for NSE Promoter Pledge Dataset."""

import pandas as pd
from pathlib import Path

def audit_quality():
    print("=" * 65)
    print(" NSE PROMOTER PLEDGE & OWNERSHIP - DATA QUALITY AUDIT")
    print("=" * 65)

    parquet_path = Path(__file__).parent / "output" / "promoter_pledge_ownership.parquet"
    assert parquet_path.exists(), f"Missing {parquet_path.name}"

    df = pd.read_parquet(parquet_path)
    print(f"Total Ownership Records Indexed: {len(df):,}")

    null_syms = df["symbol"].isnull().sum()
    null_dates = df["quarter_ended"].isnull().sum()
    null_promoters = df["promoter_holding_pct"].isnull().sum()
    null_pledges = df["promoter_pledged_pct"].isnull().sum()

    print(f"Null Symbols: {null_syms} {'[PASS]' if null_syms == 0 else '[FAIL]'}")
    print(f"Null Quarter Dates: {null_dates} {'[PASS]' if null_dates == 0 else '[FAIL]'}")
    print(f"Null Promoter Holdings: {null_promoters} {'[PASS]' if null_promoters == 0 else '[FAIL]'}")
    print(f"Null Pledged Shares %: {null_pledges} {'[PASS]' if null_pledges == 0 else '[FAIL]'}")

    # Range checks: percentages must be within 0.0 to 100.0
    invalid_promoters = ((df["promoter_holding_pct"] < 0.0) | (df["promoter_holding_pct"] > 100.0)).sum()
    invalid_pledges = ((df["promoter_pledged_pct"] < 0.0) | (df["promoter_pledged_pct"] > 100.0)).sum()
    print(f"Invalid Promoter Holding Range (<0 or >100): {invalid_promoters} {'[PASS]' if invalid_promoters == 0 else '[FAIL]'}")
    print(f"Invalid Pledged Pct Range (<0 or >100): {invalid_pledges} {'[PASS]' if invalid_pledges == 0 else '[FAIL]'}")

    # Risk breakdown
    print("\nOwnership Records by Pledge Risk Tier:")
    for tier, cnt in df["pledge_risk_category"].value_counts().items():
        print(f"  • {tier:<28}: {cnt:>4} scrips")

    assert null_syms == 0, "Symbols contain nulls!"
    assert null_dates == 0, "Dates contain nulls!"
    assert invalid_promoters == 0, "Promoter holding out of bounds!"
    assert invalid_pledges == 0, "Promoter pledge out of bounds!"

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)

if __name__ == "__main__":
    audit_quality()
