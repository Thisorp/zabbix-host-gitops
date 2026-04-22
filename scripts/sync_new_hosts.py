import json
import glob
from lib.zbx import call, get_host, get_group_ids, get_template_ids

files = sorted(glob.glob("desired-state/hosts/*.json"))

if not files:
    print("No host files found in desired-state/hosts")
    raise SystemExit(0)

for f in files:
    with open(f, encoding="utf-8") as fh:
        data = json.load(fh)

    name = data["host"]

    if get_host(name):
        print(f"[SKIP] {name} already exists")
        continue

    print(f"[CREATE] {name}")

    payload = {
        "host": name,
        "name": data.get("visible_name", name),
        "groups": get_group_ids(data["groups"]),
        "templates": get_template_ids(data["templates"]),
        "interfaces": data["interfaces"],
        "tags": data.get("tags", []),
        "description": data.get("description", ""),
        "status": data.get("status", 0),
        "macros": data.get("macros", [])
    }

    result = call("host.create", payload)
    print(f"[OK] {name} -> {result}")