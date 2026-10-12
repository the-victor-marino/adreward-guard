from concurrent.futures import ThreadPoolExecutor
import pytest
from adreward_guard.store import RewardStore

def test_duplicate_event_survives_store_restart(tmp_path):
    path = tmp_path / "reward.db"
    assert RewardStore(path).grant("tx-1", "alice", 100, verified=True)
    assert not RewardStore(path).grant("tx-1", "alice", 100, verified=True)
    assert RewardStore(path).balance("alice") == 100

def test_unverified_event_is_not_credited(tmp_path):
    store = RewardStore(tmp_path / "rewards.db")
    assert not store.grant("fake", "alice", 100, verified=False)
    assert store.balance("alice") == 0

def test_conflicting_replay_rejected(tmp_path):
    store = RewardStore(tmp_path / "rewards.db")
    store.grant("tx-1", "alice", 100, verified=True)
    with pytest.raises(ValueError, match="conflicts"):
        store.grant("tx-1", "bob", 100, verified=True)

def test_concurrent_duplicate_callbacks_credit_once(tmp_path):
    path = tmp_path / "rewards.db"
    store = RewardStore(path)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: store.grant("tx-1", "alice", 100, verified=True), range(20)))
    assert sum(results) == 1
    assert store.balance("alice") == 100
    assert store.count() == 1
