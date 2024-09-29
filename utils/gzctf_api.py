import requests
import os

BASE_URL = "https://ctf.seusus.com"
COOKIE = f"GZCTF_Token={os.environ.get('gzctf_token')}"
GAME_ID = 1

DEFAULT_CHALLENGE_INFO = {
    "originalScore": 500,
    "isEnabled": False,
}

DEFAULT_CONTAINER_INFO = {
    "cpuCount": 1,
    "memoryLimit": 64,
    "storageLimit": 256,
}

ChallengeCategory = {"Misc", "Crypto", "Pwn", "Web", "Reverse"}
ChallengeType = {
    "StaticAttachment",
    "DynamicAttachment",
    "StaticContainer",
    "DynamicContainer",
}


def api_get_game_challenges():
    response = requests.get(
        f"{BASE_URL}/api/edit/games/{GAME_ID}/challenges",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
    ).json()
    return response


def api_get_game_details():
    response = requests.get(
        f"{BASE_URL}/api/game/{GAME_ID}/details",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
    ).json()
    return response


def api_add_game_challenge(challenge):
    assert challenge["tag"] in ChallengeCategory
    assert challenge["type"] in ChallengeType
    response = requests.post(
        f"{BASE_URL}/api/edit/games/{GAME_ID}/challenges",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
        json=challenge,
    ).json()
    return response


def api_get_game_challenge(challenge_id):
    response = requests.get(
        f"{BASE_URL}/api/edit/games/{GAME_ID}/challenges/{challenge_id}",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
    ).json()
    return response


def api_update_game_challenge(challenge_id, challenge):
    response = requests.put(
        f"{BASE_URL}/api/edit/games/{GAME_ID}/challenges/{challenge_id}",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
        json=challenge,
    ).json()
    return response


def api_upload_asset(file_name, file_data):
    response = requests.post(
        f"{BASE_URL}/api/assets",
        headers={"Cookie": COOKIE},
        files={"files": (file_name, file_data)},
    ).json()
    return response[0]


def api_update_game_challenge_attachment(challenge_id, file_hash):
    response = requests.post(
        f"{BASE_URL}/api/edit/games/{GAME_ID}/challenges/{challenge_id}/attachment",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
        json={"attachmentType": "Local", "fileHash": file_hash},
    )
    return response


def api_update_game_challenge_flags(challenge_id, flags):
    response = requests.post(
        f"{BASE_URL}/api/edit/games/{GAME_ID}/challenges/{challenge_id}/flags",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
        json=[{"flag": flag} for flag in flags],
    )
    return response


def api_get_game_notices():
    response = requests.get(
        f"{BASE_URL}/api/game/{GAME_ID}/notices",
        headers={"Cookie": COOKIE, "Content-Type": "application/json"},
    ).json()
    return response
