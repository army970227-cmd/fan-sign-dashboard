import requests
import json
import os
from datetime import datetime, timezone, timedelta

# 設定台灣時區
tw_tz = timezone(timedelta(hours=8))
now = datetime.now(tw_tz).strftime("%Y-%m-%d %H:%M:%S")

# 監控清單
events = [
    {
        "platform": "ALL MY DAY", 
        "name": "YESUNG 藝聲 應募活動", 
        "id": "46756ad6feef74d93",
        "end_time": "2026-11-02 23:59:59"
    },
    {
        "platform": "ALL MY DAY", 
        "name": "SUNGHANBIN 高雄簽售", 
        "id": "46756ae7f90ca1eb4",
        "end_time": "2026-11-09 23:59:59"
    }
]

if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
else:
    db = {"latest": {}, "history": []}

for ev in events:
    try:
        url = f"https://allmyday.com.tw/api/product/item/{ev['id']}"
        res = requests.get(url, timeout=10).json()
        sales = res.get("data", {}).get("prod", {}).get("sales_amount")
        current_sales = sales if sales is not None else 0
        
        last_sales = db["latest"].get(ev['id'], None)
        is_ended = now > ev['end_time']
        
        if last_sales is None or current_sales != last_sales:
            diff = 0 if last_sales is None else current_sales - last_sales
            record = {
                "time": now,
                "platform": ev['platform'],
                "name": ev['name'],
                "id": ev['id'],
                "total": current_sales,
                "change": diff,
                "is_ended": is_ended
            }
            db["history"].append(record)
            db["latest"][ev['id']] = current_sales
    except Exception as e:
        print(f"抓取 {ev['name']} 失敗: {e}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)
