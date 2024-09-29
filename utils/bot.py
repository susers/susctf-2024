import requests
import atexit
import pprint
import time
import os
from gzctf_api import api_get_game_notices


def send_message(msg):
    res = requests.post(
        f"{os.environ.get('bot_url')}/send_group_msg",
        json={"group_id": 264099101, "message": msg, "auto_escape": True},
        headers={"Authorization": "Bearer susctf2024_private_token"},
    )
    return res.text


BLOOD_MAP = {
    "FirstBlood": "一血",
    "SecondBlood": "二血",
    "ThirdBlood": "三血",
}

ids = set()

try:
    with open("ids", "r") as lines:
        for i in lines:
            ids.add(int(i))
except Exception:
    pass


def exit_handler():
    with open("ids", "w") as f:
        for i in ids:
            f.write(f"{i}\n")


atexit.register(exit_handler)

while True:
    res = api_get_game_notices()
    res = sorted(res, key=lambda d: d["id"])

    for i in res:
        if int(i["id"]) in ids:
            continue

        print("Get new notice " + str(i["id"]) + ": ")
        pprint.pprint(i)
        ids.add(i["id"])

        if i["type"].find("Blood") != -1:
            msg = (
                f"恭喜 {i["values"][0]} 获得 [{i["values"][1]}]"
                + f" {BLOOD_MAP[i["type"]]} 🎉"
            )
        elif i["type"] == "Normal":
            msg = f"Notice:\n{i["values"][0]}"
        else:
            continue
        # send_message(msg)

    time.sleep(10)
