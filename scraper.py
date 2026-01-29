import feedparser, json, requests
def fetch():
    # TDnetのRSS
    d = feedparser.parse("https://www.release.tdnet.info/inbs/I_main_00.html")
    data = [{"date":e.published, "title":e.title, "url":e.link} for e in d.entries]
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
if __name__ == "__main__":
    fetch()
