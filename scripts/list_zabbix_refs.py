from lib.zbx import call

print("=== HOST GROUPS ===")
groups = call("hostgroup.get", {
    "output": ["groupid", "name"],
    "sortfield": "name"
})
for g in groups:
    print(f'{g["groupid"]}\t{g["name"]}')

print("\n=== TEMPLATES ===")
templates = call("template.get", {
    "output": ["templateid", "host", "name"],
    "sortfield": "host"
})
for t in templates:
    print(f'{t["templateid"]}\t{t["host"]}')