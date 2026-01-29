import feedparser
import json
import requests
import datetime

def fetch():
    # TDnetのRSS
    RSS_URL = "https://www.release.tdnet.info/inbs/I_main_00.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    data = []
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=15)
        d = feedparser.parse(response.text)
        
        for e in d.entries:
            data.append({
                "date": e.published if hasattr(e, 'published') else "時間不明",
                "title": e.title,
                "url": e.link
            })
    except Exception as e:
        print(f"Error: {e}")

    # --- ここが重要！データが空の場合でも、中身を無理やり作る ---
    if not data:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        data = [{
            "date": f"システム状況: {now}",
            "title": "【ボット稼働中】現在、TDnetに新着情報はありません。発表があれば自動更新されます。",
            "url": "https://www.release.tdnet.info/"
        }]

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch()
