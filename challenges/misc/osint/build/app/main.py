import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from anyio import Path
import mimetypes

from base64 import b64decode
from nacl.signing import VerifyKey
from hashlib import sha256
from typing import Optional
import os
import time
import hmac

if USE_TEAM_HASH := "SUSCTF_FLAG_CONFIG" in os.environ:
    PUBLIC_KEY, CHAL_SALT, CHAL_ID = os.environ.get("SUSCTF_FLAG_CONFIG").split("@")
FLAG = os.environ.get("GZCTF_FLAG") or "susctf{test_flag}"

def verify_token(token: str) -> bool:
    verify_key = VerifyKey(b64decode(PUBLIC_KEY))
    data = f"GZCTF_TEAM_{token.split(':')[0]}".encode()
    try:
        verify_key.verify(data, b64decode(token.split(':')[1]))
        return True
    except:
        return False
    
def get_team_hash(team_token: str) -> str:
    str_sha256 = lambda s: sha256(s.encode()).hexdigest()
    return str_sha256(f"{CHAL_SALT}::{team_token}")[12:24]

def get_flag(team_token: Optional[str] = None) -> str:
    if not USE_TEAM_HASH:
        return FLAG
    else:
        team_hash = get_team_hash(team_token)
        return FLAG.replace("[TEAM_HASH]", team_hash)
    
record = {}

def check_rate(token: str) -> bool:
    if not USE_TEAM_HASH:
        token = "default"
    if token in record and time.time() - record[token] < 10:
        return False
    record[token] = time.time()
    return True

def verify_pow(data: str, proof: str, token: str) -> bool:
    print(proof + "|" + data)
    hash = hmac.new(token.encode(), (proof + "|" + data).encode(), 'sha512').hexdigest()
    print(hash)
    return hash[:5] == "00000"

mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnswerModel(BaseModel):
    a1: str
    a2: str

class PowModel(BaseModel):
    answer: AnswerModel
    proof: str
    token: Optional[str] = None

@app.post("/submit")
async def submit(post_data: PowModel):
    if not verify_pow(post_data.answer.model_dump_json(), post_data.proof, post_data.token):
        return { "error": "proof不正确" }
    if USE_TEAM_HASH and not verify_token(post_data.token):
        return { "error": "token不正确" }
    if not check_rate(post_data.token):
        return { "error": "操作过于频繁" }
    user_answer = post_data.answer
    # 答案校验部分
    if len(user_answer.a1) > 10 or len(user_answer.a2) > 10:
        return { "error": "格式不正确" }
    try:
        if user_answer.a1 == "HO2363" and user_answer.a2 == "嘉陵江":
            return { "data": get_flag() }
        else:
            return { "error": "回答错误" }
    except:
        return { "error": "内部错误" }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return await Path("index.html").read_text(encoding="utf-8")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
