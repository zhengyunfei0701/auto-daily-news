import json
import os
import requests
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")

def build_prompt(news):
    text = ""
    for i, n in enumerate(news[:50]):
        text += f"{i+1}. {n['title']}\n{n['summary']}\n{n['link']}\n\n"

    prompt = f"""
    你是汽车行业分析师。

    请将以下新闻进行分类，并筛选每类最重要的5条。

    分类如下：
    - 新能源
    - 智能驾驶
    - 政策法规
    - 国际车企
    
    要求：
    1. 必须严格输出 JSON 格式
    2. 每条包含：title, summary, link
    3. 每类最多5条
    4. 按重要性排序
    
    新闻如下：
    {text}
    
    输出格式示例：
    {{
      "新能源": [
        {{
          "title": "",
          "summary": "",
          "link": ""
        }}
      ],
      "智能驾驶": [],
      "政策法规": [],
      "国际车企": []
    }}
    """
    return prompt


def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    res = requests.post(url, json=payload)

    if res.status_code != 200:
        print(res.text)
        raise Exception("Gemini API error")

    return res.json()["candidates"][0]["content"]["parts"][0]["text"]

    res = requests.post(url, json=payload)

    if res.status_code != 200:
        print(res.text)
        raise Exception("Gemini API error")

    return res.json()["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":

    with open("news.json", "r", encoding="utf-8") as f:
        news = json.load(f)

    print(f"输入新闻数量: {len(news)}")

    prompt = build_prompt(news)

    result = call_gemini(prompt)

    with open("output/daily_raw.txt", "w", encoding="utf-8") as f:
        
        f.write(result)

    os.makedirs("output", exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")

    with open(f"output/daily_{date}.md", "w", encoding="utf-8") as f:
        f.write(result)

    print("日报生成完成")
