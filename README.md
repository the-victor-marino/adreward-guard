# AdReward Guard

[![QA tests](https://github.com/the-victor-marino/adreward-guard/actions/workflows/tests.yml/badge.svg)](https://github.com/the-victor-marino/adreward-guard/actions/workflows/tests.yml)

**Prevent duplicate, missing, and invalid mobile rewarded-ad grants.**

## Problem

A completed rewarded ad may generate retries or duplicate callbacks. A good game economy must credit an earned reward **exactly once**, without granting rewards to cancelled ads.

## Implemented QA sandbox

- Deterministic in-memory event-state tests
- **SQLite persistent** reward transactions and player balances
- Database transaction + unique transaction ID prevents concurrent double credit
- Invalid/unauthorized callback and replay tests
- FastAPI mock callback endpoint with Swagger at `/docs`
- Pytest, GitHub Actions and risk-based test strategy

The HTTP demo secret is **not** a replacement for cryptographic SSV verification and this does not connect to a live advertisement network.

## Run

```bash
python -m pip install -e ".[test]"
python -m pytest -q
ADREWARD_DB=demo.sqlite3 uvicorn adreward_guard.api:app --reload
```

On Windows PowerShell:
```powershell
$env:ADREWARD_DB="demo.sqlite3"
python -m uvicorn adreward_guard.api:app --reload
```

Try the POST `/callbacks` endpoint in Swagger UI with header `x-demo-secret: local-demo-secret` and body:

```json
{"transaction_id":"tx-100","player_id":"player-1","amount":100,"event":"completed"}
```

Send it twice: first call grants 100; second call must grant 0 additional coins.

## QA evidence

See [test strategy](docs/TEST_STRATEGY.md) for failure modes and test oracles. Reproducible defects are more valuable than a passing green badge alone.

## Important scope limits

A real AdMob integration requires canonical callback processing, ECDSA signature verification, key rotation and replay protection. This project exercises the **transaction logic using mock verification only**, not real advertising payouts.
