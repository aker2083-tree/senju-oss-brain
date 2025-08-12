from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

APP_KEY = ""  # 會從環境變數覆寫

app = FastAPI(title="Senju OSS Brain", version="0.1")

class Task(BaseModel):
    user_id: Optional[str] = None
    intent: str
    context: Optional[dict] = None

class PlanStep(BaseModel):
    action: str              # 交給「手」的動作名稱，例如: "send_telegram", "fetch_url", "binance_order"
    params: dict             # 動作參數
    when: str = "now"        # now / after / schedule

class Plan(BaseModel):
    steps: List[PlanStep]

def check_key(x_api_key: Optional[str]):
    from os import getenv
    if x_api_key is None or x_api_key != getenv("OSS_API_KEY", ""):
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/think/plan", response_model=Plan)
def think_plan(task: Task, x_api_key: Optional[str] = Header(None)):
    check_key(x_api_key)

    # 這裡可以接 LLM 做更聰明的規劃；先給最小可用策略範例
    intent = task.intent.lower()

    if "weather" in intent:
        return Plan(steps=[
            PlanStep(action="fetch_url", params={"url": "https://wttr.in/?format=3"}),
            PlanStep(action="reply_user", params={"channel": "telegram"})
        ])
    if "binance" in intent or "下單" in intent:
        return Plan(steps=[
            PlanStep(action="binance_order", params={"symbol": "BTCUSDT", "side": "BUY", "qty": 0.001}),
            PlanStep(action="reply_user", params={"channel": "telegram"})
        ])
    # 預設丟給千手秘手部的「轉述回覆」
    return Plan(steps=[PlanStep(action="reply_user", params={"channel": "telegram", "text": f"收到任務：{task.intent}"})])
