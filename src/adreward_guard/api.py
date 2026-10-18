"""LOCAL-ONLY mock callback API. Does not verify real AdMob signatures."""
import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from adreward_guard.store import RewardStore

app = FastAPI(title="AdReward Guard", description="Mock rewarded-ad verification QA sandbox")
store = RewardStore(os.getenv("ADREWARD_DB", "adreward-demo.sqlite3"))

class Callback(BaseModel):
    transaction_id: str = Field(min_length=1)
    player_id: str = Field(min_length=1)
    amount: int = Field(gt=0)
    event: str

@app.post("/callbacks")
def receive_callback(body: Callback, x_demo_secret: str | None = Header(default=None)):
    if x_demo_secret != os.getenv("ADREWARD_DEMO_SECRET", "local-demo-secret"):
        raise HTTPException(status_code=403, detail="unauthorized callback")
    if body.event != "completed":
        if body.event in ("cancelled", "failed"):
            return {"granted": False}
        raise HTTPException(status_code=422, detail="unsupported event")
    try:
        granted = store.grant(body.transaction_id, body.player_id, body.amount, verified=True)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"granted": granted, "balance": store.balance(body.player_id)}

@app.get("/players/{player_id}/balance")
def balance(player_id: str):
    return {"player_id": player_id, "balance": store.balance(player_id)}
