# 🚀 Zabbix Host GitOps (Create-Only)

## 🎯 Mục tiêu

Quản lý việc **tạo host mới trên Zabbix bằng GitOps**:

* Không thao tác trên UI
* Không sửa host đã tồn tại
* Mọi thay đổi đều qua Git (traceable, audit được)
* Có CI/CD validate + plan + apply

---

## 🧱 Kiến trúc

```text
Git (GitHub)
   ↓
Pull Request → Validate + Plan
   ↓
Merge → Manual Apply
   ↓
Zabbix API (host.create)
```

---

## 📁 Cấu trúc repo

```text
.
├── desired-state/
│   └── hosts/              # 🔥 nơi khai báo host
│       ├── app-172.16.6.17.json
│       ├── fortigate-test.json
│       └── ...
├── scripts/
│   ├── sync_new_hosts.py   # create host (idempotent)
│   ├── list_zabbix_refs.py # list group/template
│   └── lib/zbx.py          # wrapper Zabbix API
├── .github/workflows/      # CI/CD
├── requirements.txt
└── README.md
```

---

## ⚙️ Nguyên tắc hoạt động

### ✅ Create-only (rất quan trọng)

| Trạng thái host | Hành động |
| --------------- | --------- |
| Chưa tồn tại    | ➜ CREATE  |
| Đã tồn tại      | ➜ SKIP    |

👉 Không bao giờ:

* update host
* xóa host
* override config từ UI

---

## 📌 Format host JSON

### Linux (Zabbix Agent)

```json
{
  "host": "app-172.16.6.17",
  "visible_name": "app-172.16.6.17",
  "groups": ["Applications", "Linux servers"],
  "templates": ["Linux by Zabbix agent"],
  "interfaces": [
    {
      "type": 1,
      "main": 1,
      "useip": 1,
      "ip": "172.16.6.17",
      "dns": "",
      "port": "10050"
    }
  ],
  "tags": [
    { "tag": "managed_by", "value": "gitops" }
  ]
}
```

---

### SNMP (Generic)

```json
{
  "host": "snmp-172.16.6.20",
  "groups": ["Network devices"],
  "templates": ["Generic by SNMP"],
  "interfaces": [
    {
      "type": 2,
      "main": 1,
      "useip": 1,
      "ip": "172.16.6.20",
      "port": "161",
      "details": {
        "version": 2,
        "community": "{$SNMP_COMMUNITY}"
      }
    }
  ],
  "macros": [
    {
      "macro": "{$SNMP_COMMUNITY}",
      "value": "public"
    }
  ]
}
```

---

### FortiGate

```json
{
  "host": "fw-fortigate-01",
  "groups": ["Network devices"],
  "templates": ["FortiGate by SNMP"],
  "interfaces": [
    {
      "type": 2,
      "main": 1,
      "useip": 1,
      "ip": "172.16.1.10",
      "port": "161",
      "details": {
        "version": 2,
        "community": "{$SNMP_COMMUNITY}"
      }
    }
  ],
  "macros": [
    { "macro": "{$SNMP_COMMUNITY}", "value": "public" }
  ]
}
```

---

### Juniper

```json
{
  "host": "router-juniper-01",
  "groups": ["Network devices"],
  "templates": ["Juniper by SNMP"],
  "interfaces": [
    {
      "type": 2,
      "main": 1,
      "useip": 1,
      "ip": "172.16.1.20",
      "port": "161",
      "details": {
        "version": 2,
        "community": "{$SNMP_COMMUNITY}"
      }
    }
  ],
  "macros": [
    { "macro": "{$SNMP_COMMUNITY}", "value": "public" }
  ]
}
```

---

## 🔐 Cấu hình môi trường

### Local (.env)

```bash
ZABBIX_URL=http://172.16.0.2:8080/api_jsonrpc.php
ZABBIX_TOKEN=your_token_here
```

---

### GitHub Secrets

| Key          | Value          |
| ------------ | -------------- |
| ZABBIX_URL   | Zabbix API URL |
| ZABBIX_TOKEN | API Token      |

---

## 🧪 Chạy local

```bash
pip install -r requirements.txt
python scripts/sync_new_hosts.py
```

---

## 🔍 Lấy danh sách group / template

```bash
python scripts/list_zabbix_refs.py
```

---

## 🌐 CI/CD (GitHub Actions)

### Flow:

#### 1. Pull Request

* validate JSON
* plan host

```text
[PLAN][CREATE] host-a
[PLAN][SKIP] host-b
```

---

#### 2. Merge vào main

* chạy validate + plan lại

---

#### 3. Apply (manual)

Vào:

```
Actions → Run workflow → apply=true
```

👉 sẽ chạy:

```bash
python scripts/sync_new_hosts.py
```

---

## 🔒 Best Practices

### 1. Không sửa host trên UI

→ sẽ drift khỏi Git

---

### 2. Không hardcode SNMP community

❌ Sai:

```json
"community": "public"
```

✅ Đúng:

```json
"community": "{$SNMP_COMMUNITY}"
```

---

### 3. Luôn gắn tag

```json
{ "tag": "managed_by", "value": "gitops" }
```

---

### 4. Mỗi host = 1 file

---

### 5. Template theo vendor

| Vendor    | Template              |
| --------- | --------------------- |
| Linux     | Linux by Zabbix agent |
| FortiGate | FortiGate by SNMP     |
| Juniper   | Juniper by SNMP       |

---

## ⚠️ Troubleshooting

### ❌ Missing group/template

```text
Missing host groups in Zabbix
```

👉 chạy:

```bash
python scripts/list_zabbix_refs.py
```

---

### ❌ API lỗi

```text
Session terminated
```

👉 kiểm tra:

* token
* Authorization header

---

### ❌ Host không tạo

👉 check log CI:

```text
[SKIP] host already exists
```

---

## 🚀 Roadmap (optional)

* [ ] Auto detect template theo vendor
* [ ] Drift detection (Zabbix vs Git)
* [ ] Export host → Git
* [ ] Bulk import

---

## 👨‍💻 Author

SRE - VNPost
Managed by GitOps 🚀
