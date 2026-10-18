import pytest
from fastapi.testclient import TestClient
from adreward_guard import api
from adreward_guard.store import RewardStore

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "store", RewardStore(tmp_path / "api.sqlite3"))
    return TestClient(api.app)

def test_api_idempotency_and_balance(client):
    payload = {"transaction_id":"tx-001","player_id":"player-1","amount":100,"event":"completed"}
    headers = {"x-demo-secret":"local-demo-secret"}
    first = client.post("/callbacks", json=payload, headers=headers)
    second = client.post("/callbacks", json=payload, headers=headers)
    assert first.status_code == 200 and first.json()["granted"] is True
    assert second.status_code == 200 and second.json()["granted"] is False
    assert client.get("/players/player-1/balance").json()["balance"] == 100

def test_api_rejects_unauthorized_callback(client):
    assert client.post("/callbacks", json={"transaction_id":"tx","player_id":"p","amount":100,"event":"completed"}).status_code == 403

def test_cancelled_ad_gives_no_reward(client):
    r = client.post("/callbacks",json={"transaction_id":"tx","player_id":"p","amount":100,"event":"cancelled"},headers={"x-demo-secret":"local-demo-secret"})
    assert r.json()["granted"] is False
    assert client.get("/players/p/balance").json()["balance"] == 0
