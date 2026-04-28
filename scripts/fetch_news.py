import feedparser
import json
import os
from datetime import datetime

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


def get_run_date():
    return os.environ.get("RUN_DATE") or datetime.now().strftime("%Y-%m-%d")


def get_output_dir():
    return os.path.join("output", get_run_date())


if __name__ == "__main__":
    data = fetch_news()

    print("总新闻数:", len(data))

    output_dir = get_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    news_path = os.path.join(output_dir, "news.json")

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成 {news_path}")