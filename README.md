# AdReward Guard

**Automated QA for rewarded-ad integrity in mobile games.**

Rewarded ads should credit the promised amount **once per verified transaction**. Duplicate callbacks, cancelled ads and invalid reward amounts are common risk scenarios worth testing.

## Current MVP (simulated)

A small in-memory reward ledger and deterministic Pytest suite cover completed ads, duplicate callbacks, cancellation, failure and invalid amounts. This is an **offline prototype**, not a production integration with AdMob/Unity Ads. Production verification would require server-side validation, durable storage and atomic transaction handling.

## Run

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

## Roadmap

1. Persist transactions with SQLite and enforce uniqueness in storage.
2. Model pending/completed/failed transaction states.
3. Simulate delayed, reordered and replayed callbacks.
4. Add FastAPI endpoints, tests and structured defect reports.
5. Verify a sandbox/mock SDK integration.

## Evidence

CI runs the deterministic tests on every PR; real ad-network claims are out of scope for the current MVP.
