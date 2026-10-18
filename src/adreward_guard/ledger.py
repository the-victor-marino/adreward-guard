"""Deterministic rewarded-ad simulator; not a live ad SDK integration."""
from dataclasses import dataclass, field

@dataclass
class RewardLedger:
    balance: int = 0
    granted_transactions: set[str] = field(default_factory=set)

    def apply(self, transaction_id: str, event: str, coins: int = 100) -> bool:
        """Return True only when a completed transaction grants a reward."""
        if not isinstance(transaction_id, str) or not transaction_id.strip():
            raise ValueError("transaction_id is required")
        if isinstance(coins, bool) or not isinstance(coins, int) or coins <= 0:
            raise ValueError("coins must be a positive integer")
        if event not in {"completed", "cancelled", "failed"}:
            raise ValueError("unknown event")
        if event != "completed" or transaction_id in self.granted_transactions:
            return False
        self.balance += coins
        self.granted_transactions.add(transaction_id)
        return True
