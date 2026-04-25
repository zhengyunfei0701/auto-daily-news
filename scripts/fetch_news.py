import feedparser
import json

RSS_FEEDS = [
    "https://www.reuters.com/rssFeed/businessNews",
    "https://electrek.co/feed/",
    "https://insideevs.com/rss/category/news/",
]

def fetch_news():
    news = []

    for url in RSS_FEEDS:
        print(f"正在抓取: {url}")

        feed = feedparser.parse(url)

        print("条目数:", len(feed.entries))

        for entry in feed.entries[:10]:
            news.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")
            })

    return news


if __name__ == "__main__":
    data = fetch_news()

    print("总新闻数:", len(data))

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)