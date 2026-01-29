import feedparser
import json

def fetch():
    # TDnetのメインRSS（ここが一番安定しています）
    RSS_URL = "https://www.release.tdnet.info/inbs/I_main_00.html"
    
    # データを解析
    d = feedparser.parse(RSS_URL)
    
    # 1件も取れなかった場合のエラー回避
    if not d.entries:
        print("現在、新しい開示情報はありません。")
        # テスト用に「準備完了」のダミーデータを入れることも可能
        data = [{"date": "確認中", "title": "現在、新着情報はありません。しばらくお待ちください。", "url": "#"}]
    else:
        # 正常に取得できた場合
        data = []
        for e in d.entries:
            data.append({
                "date": e.published if hasattr(e, 'published') else "不明",
                "title": e.title,
                "url": e.link
            })
    
    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch()
