"""SQLite reward ledger with atomic, idempotent grants (local simulation)."""
import sqlite3
from pathlib import Path

class RewardStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS rewards (tx TEXT PRIMARY KEY, player TEXT NOT NULL, amount INTEGER NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS balances (player TEXT PRIMARY KEY, amount INTEGER NOT NULL DEFAULT 0)")

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.execute("PRAGMA busy_timeout=10000")
        return db

    def grant(self, tx: str, player: str, amount: int, *, verified: bool) -> bool:
        if not verified:
            return False
        if not all(isinstance(x, str) and x.strip() for x in (tx, player)):
            raise ValueError("transaction and player required")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be positive integer")
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT player, amount FROM rewards WHERE tx=?", (tx,)).fetchone()
            if row is not None:
                if row != (player, amount):
                    raise ValueError("replayed transaction conflicts with original reward")
                return False
            db.execute("INSERT INTO rewards VALUES (?,?,?)", (tx, player, amount))
            db.execute("INSERT INTO balances(player,amount) VALUES (?,?) ON CONFLICT(player) DO UPDATE SET amount=amount+excluded.amount", (player, amount))
        return True

    def balance(self, player: str) -> int:
        with self._connect() as db:
            row = db.execute("SELECT amount FROM balances WHERE player=?", (player,)).fetchone()
        return row[0] if row else 0

    def count(self) -> int:
        with self._connect() as db:
            return db.execute("SELECT count(*) FROM rewards").fetchone()[0]
