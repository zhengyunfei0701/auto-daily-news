import feedparser
import json
import os

RSS_FEEDS = [
    "https://www.reuters.com/rssFeed/businessNews",
    "https://electrek.co/feed/",
    "https://insideevs.com/rss/category/news/",
]

def get_link(entry):
    # 1. 标准 RSS
    if hasattr(entry, "link") and entry.link:
        return entry.link

    # 2. Atom / 多链接结构
    if hasattr(entry, "links") and entry.links:
        return entry.links[0].get("href", "")

    # 3. fallback id
    if hasattr(entry, "id"):
        return entry.id

    return ""

def fetch_news():
    news = []

    for url in RSS_FEEDS:
        print(f"正在抓取: {url}")

        feed = feedparser.parse(url)

        print("条目数:", len(feed.entries))

        for entry in feed.entries[:10]:
            news.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": get_link(entry)
            })

    return news


if __name__ == "__main__":
    data = fetch_news()

    print("总新闻数:", len(data))

    # ✅ 强制创建目录（关键）
    os.makedirs("output", exist_ok=True)

    # ✅ 写入标准路径（统一 pipeline）
    with open("output/news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 已生成 output/news.json")