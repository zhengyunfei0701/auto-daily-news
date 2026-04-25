import json
from datetime import datetime

CATEGORIES = {
    "新能源": "新能源",
    "智能驾驶": "智能驾驶",
    "政策法规": "政策法规",
    "国际车企": "国际车企"
}

def build_md(data):
    date = datetime.now().strftime("%Y-%m-%d")

    md = f"# 汽车行业日报 {date}\n\n"

    for cat, title in CATEGORIES.items():
        md += f"## {title}\n\n"

        items = data.get(cat, [])[:5]

        if not items:
            md += "_暂无数据_\n\n"
            continue

        for i, item in enumerate(items, 1):
            md += f"{i}. **{item['title']}**\n"
            md += f"   {item['summary']}\n"
            md += f"   🔗 {item['link']}\n\n"

    md += "\n---\n## 今日总结（AI生成）\n\n"
    md += "（后续可加趋势总结模块）\n"

    return md


if __name__ == "__main__":
    with open("output/daily_structured.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    md = build_md(data)

    with open("output/daily_final.md", "w", encoding="utf-8") as f:
        f.write(md)

    print("Markdown生成完成")
