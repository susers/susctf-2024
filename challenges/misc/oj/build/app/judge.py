import subprocess
from typing import Tuple

def compile(code: str) -> Tuple[bool, str]:
    with open("temp/temp.cpp", "wb") as f, open("static/template.h", "rb") as template_file:
        template = template_file.read()
        code_bytes = code.replace("\r", "").encode("utf-8", errors="ignore")
        data = template.replace(b"{{ code }}", code_bytes)
        f.write(data)
        f.close()
    try:
        result = subprocess.check_output([*"g++ -o temp/code".split(" "), f.name, "-lseccomp"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return False, e.output.decode("utf-8", errors="ignore")
    return True, result.decode("utf-8", errors="ignore")

def run() -> Tuple[bool, str, str]:
    try:
        result = subprocess.check_output(["./temp/code"], stderr=subprocess.STDOUT, timeout=1).decode("utf-8", errors="ignore")
        if not result.strip().isdigit():
            return False, "输出格式错误", result
        if int(result)!= 3:
            return False, "答案错误", result
        return True, "答案正确", result
    except subprocess.CalledProcessError as e:
        return False, "运行失败", e.output.decode("utf-8", errors="ignore")