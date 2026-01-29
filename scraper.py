import requests
from bs4 import BeautifulSoup
import json
import datetime

def fetch():
    # 教えていただいたURL
    URL = "https://www.release.tdnet.info/inbs/I_main_00.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    data = []
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.encoding = response.apparent_encoding
        
        # HTMLを解析してテーブルの行を取得
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr') # 行(tr)をすべて探す
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5: # 必要なデータが揃っている行だけ処理
                date = cols[0].get_text(strip=True)
                time = cols[1].get_text(strip=True)
                code = cols[2].get_text(strip=True)
                name = cols[3].get_text(strip=True)
                title = cols[4].get_text(strip=True)
                # PDFリンクを取得
                link_tag = cols[4].find('a')
                url = "https://www.release.tdnet.info/inbs/" + link_tag.get('href') if link_tag else "#"
                
                data.append({
                    "date": f"{date} {time}",
                    "name": name,
                    "code": code,
                    "title": title,
                    "url": url
                })
    except Exception as e:
        print(f"Error: {e}")

    # もし空ならメッセージを入れる
    if not data:
        data = [{"date": "確認中", "title": "現在、新着情報が取得できません。URLの構造が変わった可能性があります。", "url": "#"}]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch()
