import json
from datetime import datetime


CATEGORIES = [
    "新能源",
    "智能驾驶",
    "政策法规",
    "国际车企"
]


def build_md(data):
    date = datetime.now().strftime("%Y-%m-%d")

    md = f"# 汽车行业日报 {date}\n\n"

    # ======================
    # 1️⃣ 先输出核心趋势（最重要）
    # ======================
    md += "## 今日核心趋势\n\n"

    trends = data.get("trends", [])

    if trends:
        for i, t in enumerate(trends, 1):
            md += f"{i}. {t}\n"
    else:
        md += "暂无趋势数据\n"

    md += "\n---\n"

    # ======================
    # 2️⃣ 再输出详细分类
    # ======================

    for cat in CATEGORIES:
        md += f"## {cat}\n\n"

        items = data.get(cat, [])[:5]

        if not items:
            md += "暂无数据\n\n"
            continue

        for i, item in enumerate(items, 1):
            md += f"{i}. **{item['title']}**\n"
            md += f"   {item['summary']}\n"
            md += f"   {item['link']}\n\n"

    return md


if __name__ == "__main__":
    with open("output/daily_structured.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    md = build_md(data)

    with open("output/daily_final.md", "w", encoding="utf-8") as f:
        f.write(md)

    print("日报生成完成")
