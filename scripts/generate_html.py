import json
from datetime import datetime

CATEGORIES = ["新能源", "智能驾驶", "政策法规", "国际车企"]


def _normalize_title(title):
    return " ".join((title or "").strip().lower().split())


def build_link_map(news_items):
    link_map = {}
    for item in news_items:
        key = _normalize_title(item.get("title", ""))
        link = (item.get("link") or "").strip()
        if key and link and key not in link_map:
            link_map[key] = link
    return link_map


def render_category(cat, items, fallback_link_map):
    cards = ""
    for idx, item in enumerate(items[:5], 1):
        raw_title = item.get("title", "")
        summary = item.get("summary", "暂无摘要")

        link = (item.get("link") or "").strip()
        if not link and fallback_link_map:
            link = fallback_link_map.get(_normalize_title(raw_title), "")

        link_html = (
            f'<a class="inline-link" href="{link}" target="_blank" rel="noopener noreferrer">阅读原文</a>'
            if link else
            '<span class="inline-link disabled">（链接缺失）</span>'
        )

        cards += f"""
        <li class="news-card">
            <div class="news-index">{idx}</div>
            <div class="news-content">
                <p class="news-body">{summary} {link_html}</p>
            </div>
        </li>
        """

    if not cards:
        cards = '<li class="empty">暂无相关新闻</li>'

    return f"""
    <section class="section-block">
        <h3>{cat}</h3>
        <ol class="news-list">
            {cards}
        </ol>
    </section>
    """


def md_to_wechat_html(data, fallback_link_map=None):
    date = datetime.now().strftime("%Y-%m-%d")
    trends = "".join(f"<li>{t}</li>" for t in data.get("trends", []))
    if not trends:
        trends = "<li>今日暂无趋势数据</li>"

    sections_html = "".join(
        render_category(cat, data.get(cat, []), fallback_link_map)
        for cat in CATEGORIES
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>汽车行业日报 {date}</title>
  <style>
    :root {{
      --bg: #f5f7fb;
      --card: #ffffff;
      --text: #1f2937;
      --sub: #4b5563;
      --brand: #2563eb;
      --border: #e5e7eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.65;
    }}
    .page {{
      max-width: 760px;
      margin: 0 auto;
      padding: 14px 12px 28px;
    }}
    .hero {{
      background: linear-gradient(135deg, #1d4ed8, #2563eb);
      color: #fff;
      border-radius: 16px;
      padding: 16px 14px;
      box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
      margin-bottom: 12px;
    }}
    .hero h1 {{
      margin: 0;
      font-size: 20px;
      line-height: 1.4;
    }}
    .hero .date {{
      margin-top: 4px;
      font-size: 13px;
      opacity: 0.9;
    }}
    .section-block {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px;
      margin-top: 12px;
    }}
    .section-block h3 {{
      margin: 0 0 10px;
      font-size: 18px;
      color: #111827;
    }}
    .trend-list {{
      margin: 0;
      padding-left: 20px;
      color: var(--sub);
    }}
    .trend-list li + li {{
      margin-top: 8px;
    }}
    .news-list {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}
    .news-card {{
      display: flex;
      gap: 10px;
      padding: 10px 0;
      border-top: 1px dashed var(--border);
    }}
    .news-card:first-child {{
      border-top: none;
      padding-top: 0;
    }}
    .news-index {{
      flex: 0 0 auto;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #dbeafe;
      color: var(--brand);
      font-size: 13px;
      font-weight: 700;
      text-align: center;
      line-height: 24px;
      margin-top: 2px;
    }}
    .news-body {{
      margin: 0 0 10px;
      color: var(--sub);
      font-size: 14px;
    }}
    .inline-link {{
      text-decoration: none;
      color: var(--brand);
      font-size: 14px;
      font-weight: 600;
      white-space: nowrap;
    }}
    .inline-link.disabled {{
      color: #9ca3af;
      font-weight: 400;
    }}
    .empty {{
      color: #9ca3af;
      font-size: 14px;
      padding: 4px 0;
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <h1>汽车行业日报</h1>
      <div class="date">{date}</div>
    </header>

    <section class="section-block">
      <h3>今日核心趋势</h3>
      <ol class="trend-list">
        {trends}
      </ol>
    </section>

    {sections_html}
  </main>
</body>
</html>"""


if __name__ == "__main__":
    with open("output/daily_structured.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    link_map = {}
    try:
        with open("output/news.json", "r", encoding="utf-8") as f:
            source_news = json.load(f)
            link_map = build_link_map(source_news)
    except FileNotFoundError:
        pass

    html = md_to_wechat_html(data, fallback_link_map=link_map)

    with open("output/wechat.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("公众号HTML生成完成")