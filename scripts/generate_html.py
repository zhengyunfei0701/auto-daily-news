import json
from datetime import datetime

def md_to_wechat_html(data):
    date = datetime.now().strftime("%Y-%m-%d")

    html = f"<h2>汽车行业日报 {date}</h2>"

    # 趋势
    html += "<h3>今日核心趋势</h3><ol>"
    for t in data.get("trends", []):
        html += f"<li>{t}</li>"
    html += "</ol>"

    # 分类
    for cat in ["新能源", "智能驾驶", "政策法规", "国际车企"]:
        html += f"<h3>{cat}</h3><ol>"

        for item in data.get(cat, [])[:5]:
            html += f"""
            <li>
                <b>{item['title']}</b><br/>
                {item['summary']}<br/>
                <a href="{item['link']}">原文链接</a>
            </li>
            """

        html += "</ol>"

    return html


if __name__ == "__main__":
    with open("output/daily_structured.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    html = md_to_wechat_html(data)

    with open("output/wechat.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("公众号HTML生成完成")