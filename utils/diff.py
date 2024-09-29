import os
import json

ALL_CHANGED_FILES = os.environ.get('ALL_CHANGED_FILES') or ""

ALL_CHANGED_FILES = ALL_CHANGED_FILES.split(" ")

target_dir = set()
target_need_build = {}
for file in ALL_CHANGED_FILES:
    if file.startswith("challenges/"):
        path_list = file.split("/")
        chanllenge_path = "/".join(path_list[:3])
        target_dir.add(chanllenge_path)
        if len(path_list) > 2 and path_list[3] == "build":
            target_need_build[chanllenge_path] = True

print(json.dumps([{
    "root_dir": target,
    "task_name": target.split("/")[-1],
    "need_build": target_need_build.get(target, False),
} for target in target_dir]))
