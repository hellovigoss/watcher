#!/usr/bin/env python3
import os
import sys
import time
import requests
from datetime import datetime

URL = "https://api.coze.cn/v1/workflow/stream_run"
TOKEN = os.getenv("COZE_TOKEN")
WORKFLOW_ID = "7580261530635042843"
MAX_RETRY = 3
RETRY_SLEEP = 5

if not TOKEN:
    print("❌  COZE_TOKEN 未设置", file=sys.stderr)
    sys.exit(1)

payload = {"workflow_id": WORKFLOW_ID, "parameters": {}}
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

for attempt in range(1, MAX_RETRY + 1):
    print(f"[{datetime.now().isoformat()}] 第 {attempt} 次调用 …")
    try:
        r = requests.post(URL, json=payload, headers=headers, timeout=30)
        print("HTTP", r.status_code, r.text)
        if r.ok:          # 状态码 200-299
            print("✅ 成功")
            sys.exit(0)
        # 状态码异常，继续重试
    except requests.RequestException as e:
        print("⚠️  网络异常:", e)

    if attempt < MAX_RETRY:
        print(f"⏳ 等待 {RETRY_SLEEP}s 后重试 …")
        time.sleep(RETRY_SLEEP)

print("❌ 3 次均失败，退出码 1")
sys.exit(1)