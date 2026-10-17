"""CLI Tool for NSE Promoter Pledge & Ownership.

Usage:
    python runner.py --symbol VEDL
    python runner.py --high-pledge
    python runner.py --summary
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from nse_promoter_pledge_and_ownership.evaluator import GovernanceEvaluator

def main():
    parser = argparse.ArgumentParser(description="NSE Promoter Pledge & Ownership CLI")
    parser.add_argument("--symbol", help="Target equity ticker")
    parser.add_argument("--high-pledge", action="store_true", help="Filter scrips with promoter pledge >= 10%")
    parser.add_argument("--summary", action="store_true", help="Show overview of ownership database")
    args = parser.parse_args()

    parquet_path = Path(__file__).parent / "output" / "promoter_pledge_ownership.parquet"
    if not parquet_path.exists():
        print("Dataset not found. Run python update.py first.")
        return

    df = pd.read_parquet(parquet_path)
    evaluator = GovernanceEvaluator(df)

    if args.symbol:
        sym_upper = args.symbol.upper()
        sym_df = df[df["symbol"] == sym_upper]
        if sym_df.empty:
            print(f"No ownership records found for {sym_upper}.")
            return

        latest = sym_df.iloc[0]
        print(f"\n--- Shareholding & Governance Profile: {sym_upper} ---")
        print(f"  * Promoter Holding        : {latest['promoter_holding_pct']:.2f}%")
        print(f"  * Promoter Pledged Shares : {latest['promoter_pledged_pct']:.2f}%")
        print(f"  * Institutional Holding   : {latest['institutional_holding_pct']:.2f}% ({latest['institutional_holders_count']} institutions)")
        print(f"  * Public Float            : {latest['public_float_pct']:.2f}%")
        print(f"  * Pledge Risk Tier        : {latest['pledge_risk_category']}")
        is_safe = evaluator.is_safe_for_investment(sym_upper)
        print(f"  * Quant Governance Filter : {'[PASS] Low/Zero Pledge' if is_safe else '[REJECT] Elevated Encumbrance Risk'}\n")

    elif args.high_pledge:
        high_df = evaluator.filter_high_pledge_scrips(threshold_pct=10.0)
        print(f"\n--- Scrips with Elevated Promoter Pledges (>=10%) ---")
        cols = ["symbol", "promoter_holding_pct", "promoter_pledged_pct", "pledge_risk_category"]
        print(high_df[cols].to_string(index=False))
        print()

    else:
        print(f"\n==========================================================================")
        print(f" NSE PROMOTER PLEDGE & OWNERSHIP DATABASE (Showing {len(df)} scrips)")
        print(f"==========================================================================")
        cols = ["symbol", "promoter_holding_pct", "promoter_pledged_pct", "institutional_holding_pct", "pledge_risk_category"]
        print(df[cols].to_string(index=False))
        print(f"==========================================================================\n")

if __name__ == "__main__":
    main()
