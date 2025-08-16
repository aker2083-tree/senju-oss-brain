from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ThinkRequest(BaseModel):
    text: str

@app.post("/think")
def think(req: ThinkRequest):
    return {"reply": f"大腦收到: {req.text}"}

@app.get("/")
def root():
    return {"status": "大腦正常運行中"}
