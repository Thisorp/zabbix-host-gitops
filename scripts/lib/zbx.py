import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("ZABBIX_URL")
TOKEN = os.getenv("ZABBIX_TOKEN")

if not URL:
    raise Exception("Missing ZABBIX_URL")

if not TOKEN:
    raise Exception("Missing ZABBIX_TOKEN")


def call(method, params):
    headers = {
        "Content-Type": "application/json-rpc",
        "Authorization": f"Bearer {TOKEN}"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    r = requests.post(URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()

    if "error" in data:
        raise Exception(f"Zabbix API error in {method}: {data['error']}")

    return data["result"]


def get_host(name):
    result = call("host.get", {
        "filter": {"host": [name]},
        "output": ["hostid", "host", "name"]
    })
    return result[0] if result else None


def get_group_ids(names):
    result = call("hostgroup.get", {
        "output": ["groupid", "name"]
    })

    mapping = {x["name"]: x["groupid"] for x in result}
    missing = [n for n in names if n not in mapping]

    if missing:
        raise Exception(f"Missing host groups in Zabbix: {missing}")

    return [{"groupid": mapping[n]} for n in names]


def get_template_ids(names):
    result = call("template.get", {
        "output": ["templateid", "host", "name"]
    })

    mapping = {x["host"]: x["templateid"] for x in result}
    missing = [n for n in names if n not in mapping]

    if missing:
        raise Exception(f"Missing templates in Zabbix: {missing}")

    return [{"templateid": mapping[n]} for n in names]