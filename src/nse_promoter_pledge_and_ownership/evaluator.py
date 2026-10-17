"""Promoter Pledge and Governance Risk Evaluator."""

import pandas as pd
from typing import Dict, Any, List

class GovernanceEvaluator:
    """Evaluates promoter pledging risks and corporate governance filters."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def filter_high_pledge_scrips(self, threshold_pct: float = 20.0) -> pd.DataFrame:
        """Returns scrips with promoter pledges exceeding threshold %."""
        return self.df[self.df["promoter_pledged_pct"] >= threshold_pct].sort_values("promoter_pledged_pct", ascending=False)

    def is_safe_for_investment(self, symbol: str, max_allowed_pledge: float = 10.0) -> bool:
        """Quantitative filter: rejects scrips with high promoter encumbrance."""
        sym_rows = self.df[self.df["symbol"] == symbol.upper()]
        if sym_rows.empty:
            return True
        latest = sym_rows.iloc[0]
        return float(latest["promoter_pledged_pct"]) <= max_allowed_pledge
