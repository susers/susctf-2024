import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from anyio import Path
import mimetypes

from judge import *

from typing import Optional
import os
import time

record = {}

def check_rate(token: str = "default") -> bool:
    if token in record and time.time() - record[token] < 1:
        return False
    record[token] = time.time()
    return True

mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class CodeModel(BaseModel):
    code: str

@app.post("/submit")
async def submit(post_data: CodeModel):
    if not check_rate():
        return { "data": "\033[31m操作过于频繁，请稍后再试\033[0m" }
    user_code = post_data.code
    if len(user_code) > 40960:
        return { "data": "\033[31m代码过长\033[0m" }
    success, compile_result = compile(user_code)
    if not success:
        return { "data": "\033[31m编译失败\033[0m\r\n" + compile_result.replace("\n", "\r\n") }
    success, run_result, output = run()
    header = "\033[32m" if success else "\033[31m"
    return { "data": header + run_result + "\033[0m\r\n" + output.replace("\n", "\r\n") }
    

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return await Path("index.html").read_text(encoding="utf-8")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
