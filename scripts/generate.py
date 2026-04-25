import os
from datetime import datetime

def build_markdown(ai_text):
    date = datetime.now().strftime("%Y-%m-%d")

    md = f"""
# 🚗 汽车行业日报 {date}

---

{ai_text}

---

## 📌 数据来源
- RSS自动抓取
- AI自动整理

## ⚠️ 免责声明
本内容由AI自动生成，仅供参考
"""

    return md


if __name__ == "__main__":

    # 读取AI输出
    with open("output/daily_raw.txt", "r", encoding="utf-8") as f:
        ai_text = f.read()

    md = build_markdown(ai_text)

    os.makedirs("output", exist_ok=True)

    with open("output/daily_final.md", "w", encoding="utf-8") as f:
        f.write(md)

    print("公众号文章生成完成")