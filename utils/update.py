import gzctf_api as api
import pprint
import sys
import os
import tomllib
import glob
import zipfile
from io import BytesIO

CHALLENGE = {}
CHALLENGE_INFO = {}
FLAGS = []

if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} (Chanllenges dir) (Container tag)")
    exit(0)

def extract_category(dirname):
    assert dirname.split(os.path.sep)[-3] == "challenges", f"Invalid dirname {dirname}!"
    lowered_category = dirname.split(os.path.sep)[-2]
    return lowered_category[0].upper() + lowered_category[1:]


def config_merge(config, new_config, map_dict=None, optional=False):
    if not map_dict:
        return config.update(new_config)
    for target, key in map_dict.items():
        if key in new_config:
            config[target] = new_config[key]
        elif not optional:
            assert False, f"Key {key} not found in new_config"


def upload_attachment(challenge_id, file_name, data):
    asset = api.api_upload_asset(file_name, data)
    api.api_update_game_challenge_attachment(challenge_id, asset["hash"])
    print(f"上传附件到{challenge_id}: {asset['hash']}")


root_dir = os.path.abspath(sys.argv[1])

with open(os.path.join(root_dir, "challenge.toml"), "rb") as f:
    specification = tomllib.load(f)
    if "category" not in specification:
        specification["category"] = extract_category(root_dir)

has_container = "container" in specification
is_static_container = has_container and specification["container"].get("static")
is_dynamic_flag = has_container and not is_static_container

config_merge(
    CHALLENGE,
    specification,
    {
        "title": "title",
        "tag": "category",
    },
)
CHALLENGE["type"] = (
    "StaticAttachment"
    if not has_container
    else ("DynamicContainer" if is_dynamic_flag else "StaticContainer")
)

CHALLENGE_INFO["content"] = "".join(
    [
        f'**Author:** {specification["author"]} / '+ \
        f'**Difficulty:** {specification["difficulty"]}\n\n---\n\n',
        (specification.get("description") or "").strip(),
    ]
)
if is_dynamic_flag:  # flag setup
    CHALLENGE_INFO["flagTemplate"] = specification["flag"]
else:
    if isinstance(specification["flag"], str):  # TODO
        FLAGS = [specification["flag"]]
    else:
        FLAGS = specification["flag"]
CHALLENGE_INFO = api.DEFAULT_CHALLENGE_INFO | CHALLENGE_INFO

if has_container:
    container = specification["container"]
    CHALLENGE_INFO = api.DEFAULT_CONTAINER_INFO | CHALLENGE_INFO
    config_merge(
        CHALLENGE_INFO,
        container,
        {
            "containerExposePort": "port",
            "memoryLimit": "memory",
            "storageLimit": "storage",
            "cpuCount": "cpu",
            "containerImage": "image",
        },
        optional=True,
    )
    if len(sys.argv) == 3:
        CHALLENGE_INFO["containerImage"] = sys.argv[-1]

pprint.pprint(specification)
pprint.pprint(CHALLENGE)
pprint.pprint(CHALLENGE_INFO)

assert CHALLENGE["tag"] in ["Crypto", "Misc", "Pwn", "Reverse", "Web"]

challenges = api.api_get_game_challenges()

is_exist = [
    *filter(
        lambda x: x["title"] == CHALLENGE["title"] and not x["isEnabled"], challenges
    )
]

if not is_exist:
    print(f"题目[{CHALLENGE['title']}]不存在，新建题目")
    challenge_id = api.api_add_game_challenge(CHALLENGE)["id"]
else:
    challenge_id = is_exist[0]["id"]
print(f"更新题目[{CHALLENGE['title']}] ID: {challenge_id}")
api.api_update_game_challenge(challenge_id, CHALLENGE_INFO)

# update attachment
attachments_config = specification.get("attachments") or {}
ATTACHMENTS_PATH = attachments_config.get("path") or "attachments/**"
attachments_type = "list"
attachments_name = attachments_config.get("name") or "attachments.zip"
if isinstance(ATTACHMENTS_PATH, str):
    if ATTACHMENTS_PATH.endswith(".zip"):
        attachments_type = "zip"
    else:
        ATTACHMENTS_PATH = [ATTACHMENTS_PATH]

if attachments_type == "list":
    real_attachments = []
    for path in ATTACHMENTS_PATH:
        real_attachments.extend(glob.glob(path, root_dir=root_dir, recursive=True))
    if real_attachments:
        attachment_zip = BytesIO()
        with zipfile.ZipFile(attachment_zip, "w") as z:
            for attachment in real_attachments:
                if os.path.isdir(attachment):
                    continue
                z.write(
                    os.path.join(root_dir, attachment),
                    attachment,
                )
        attachment_data = attachment_zip.getvalue()
        upload_attachment(challenge_id, attachments_name, attachment_data)
elif attachments_type == "zip":
    with open(os.path.join(root_dir, ATTACHMENTS_PATH), "rb") as f:
        attachment_data = f.read()
    upload_attachment(challenge_id, attachments_name, attachment_data)

# upload flags
if FLAGS:
    now_flags = api.api_get_game_challenge(challenge_id)["flags"]
    now_flags = [x["flag"] for x in now_flags]
    new_flags = set(FLAGS) - set(now_flags)
    if new_flags:
            api.api_update_game_challenge_flags(challenge_id, list(new_flags))
            print(f"添加静态 flag: {new_flags}")
