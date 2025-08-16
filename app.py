from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Senju OSS Brain")

class ThinkRequest(BaseModel):
    text: str

@app.get("/")
def health():
    return {"status": "ok", "service": "senju-oss-brain"}

@app.post("/think")
def think(req: ThinkRequest):
    # 這裡先回聲，之後要接真正的思考邏輯再擴充
    return {"reply": f"大腦收到：{req.text}"}
