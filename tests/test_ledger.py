import pytest
from adreward_guard.ledger import RewardLedger

def test_completed_ad_grants_reward_once():
    ledger = RewardLedger()
    assert ledger.apply("tx-1", "completed")
    assert ledger.balance == 100

def test_duplicate_callback_cannot_double_credit():
    ledger = RewardLedger()
    assert ledger.apply("tx-1", "completed")
    assert not ledger.apply("tx-1", "completed")
    assert ledger.balance == 100

@pytest.mark.parametrize("event", ["cancelled", "failed"])
def test_incomplete_ad_does_not_pay(event):
    ledger = RewardLedger()
    assert not ledger.apply("tx-1", event)
    assert ledger.balance == 0

def test_invalid_amount_rejected():
    with pytest.raises(ValueError):
        RewardLedger().apply("tx-1", "completed", coins=-100)
