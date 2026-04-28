import os
from datetime import datetime

import json


CATEGORIES = [
    "新能源",
    "智能驾驶",
    "政策法规",
    "国际车企"
]


def build_md(data):
    date = get_run_date()

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


def get_run_date():
    return os.environ.get("RUN_DATE") or datetime.now().strftime("%Y-%m-%d")


def get_output_dir():
    return os.path.join("output", get_run_date())


if __name__ == "__main__":
    output_dir = get_output_dir()
    structured_path = os.path.join(output_dir, "daily_structured.json")
    md_path = os.path.join(output_dir, "daily.md")

    if not os.path.exists(structured_path):
        print(f"❌ structured.json 不存在，跳过生成: {structured_path}")
        exit(0)

    with open(structured_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md = build_md(data)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"日报生成完成: {md_path}")
