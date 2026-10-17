"""NSE Promoter Pledge and Shareholding Ownership Package."""

from .fetcher import OwnershipFetcher
from .evaluator import GovernanceEvaluator

__all__ = ["OwnershipFetcher", "GovernanceEvaluator"]
__version__ = "0.1.0"
