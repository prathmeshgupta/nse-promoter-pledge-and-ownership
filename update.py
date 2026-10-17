"""NSE Promoter Pledge & Ownership Weekly Automated Updater.

Fetches quarterly shareholding patterns, promoter holdings, pledged shares %,
and institutional ownership, deduplicating records and exporting Parquet/CSV.
"""

import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add local src to path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from nse_promoter_pledge_and_ownership.fetcher import OwnershipFetcher

SYMBOLS_TO_MONITOR = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "BHARTIARTL", "ITC", "LT", "SBIN", "HINDUNILVR",
    "VEDL", "ADANIENT", "ADANIPORTS", "JSWENERGY",
    "GMRAIRPORT", "APOLLOHOSP", "SUZLON", "ZEEL"
]

def update_promoter_pledge():
    print(f"[{datetime.now().isoformat()}] Starting Promoter Pledge & Ownership update...")
    fetcher = OwnershipFetcher()
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "promoter_pledge_ownership.csv"
    parquet_file = output_dir / "promoter_pledge_ownership.parquet"

    existing_df = pd.DataFrame()
    if parquet_file.exists():
        existing_df = pd.read_parquet(parquet_file)
        print(f"Loaded {len(existing_df):,} existing records from {parquet_file.name}")

    records = []
    print(f"Scanning ownership and pledge encumbrance across {len(SYMBOLS_TO_MONITOR)} equities...")
    for sym in SYMBOLS_TO_MONITOR:
        row = fetcher.fetch_symbol_ownership(sym)
        if row:
            records.append(row)

    if not records and existing_df.empty:
        raise RuntimeError("No ownership records retrieved and no existing database found.")

    new_df = pd.DataFrame(records)
    combined = []
    if not existing_df.empty:
        combined.append(existing_df)
    if not new_df.empty:
        combined.append(new_df)

    merged = pd.concat(combined, ignore_index=True)

    # Core key deduplication
    merged = merged.drop_duplicates(subset=["symbol", "quarter_ended"], keep="last")

    # Sort by pledge risk descending then symbol
    merged = merged.sort_values(by=["promoter_pledged_pct", "symbol"], ascending=[False, True]).reset_index(drop=True)

    # Save
    merged.to_parquet(parquet_file, index=False, compression="snappy")
    merged.to_csv(csv_file, index=False)
    print(f"Saved {len(merged):,} ownership records to {parquet_file.name} and {csv_file.name}")

    # Run quality gate
    from evaluate_quality import audit_quality
    audit_quality()
    print("Promoter Pledge & Ownership update completed successfully.")

if __name__ == "__main__":
    update_promoter_pledge()
