from gzctf_api import api_get_game_details, api_get_game_challenge
import os
import tomllib


chals = api_get_game_details()["challenges"]

for tag in chals:
    search_dir = os.path.join("challenges", tag.lower())
    assert os.path.isdir(search_dir)
    for i in chals[tag]:
        for j in os.scandir(search_dir):
            if not os.path.isdir(j):
                continue
            with open(os.path.join(j, "challenge.toml"), "rb") as f:
                specification = tomllib.load(f)
            if specification["title"] != i["title"]:
                continue
            print(
                f"Found chal: {i["title"]}; score: {i["score"]}; solved: {i["solved"]}"
            )
            i["hints"] = api_get_game_challenge(i["id"])["hints"]
            md_str = f"""# {i["title"]}

**出题人:** `{specification["author"]}`

**题目难度:** `{specification["difficulty"]}`

**题目类型:** `{tag}`

**解出人数:** `{i["solved"]}`

**分数:** `{i["score"]}`

**flag:** `{specification["flag"]}`

## 题目描述

{specification["description"]}
{f"\n## 提示\n\n{"\n".join(["- " + j for j in i["hints"]])}\n" if i["hints"] else ""}
            """
            with open(os.path.join(j, "README.md"), "w") as f:
                f.write(md_str)
