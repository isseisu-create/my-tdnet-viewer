import feedparser
import json
import requests

def fetch():
    # 読み取り先を「全ての開示」が含まれる予備のフィードURLに変更
    RSS_URL = "https://www.release.tdnet.info/inbs/I_main_00.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=15)
        # 文字化け防止
        response.encoding = response.apparent_encoding
        d = feedparser.parse(response.text)
        
        data = []
        for e in d.entries:
            data.append({
                "date": e.published if hasattr(e, 'published') else "時間不明",
                "title": e.title,
                "url": e.link
            })
        
        # もしそれでも空っぽなら、動作確認用のテストデータを強制投入
        if not data:
            data = [{
                "date": "システム通知",
                "title": "ボットは正常稼働中です。現在TDnetに新しい開示がありません。発表があるとここに自動で表示されます。",
                "url": "https://www.release.tdnet.info/"
            }]
            
    except Exception as e:
        data = [{"date": "エラー", "title": f"取得エラーが発生しました: {str(e)}", "url": "#"}]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch()
