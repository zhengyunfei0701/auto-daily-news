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
    
    请对以下新闻进行：
    
    1. 分类整理（每类最多5条）：
    - 新能源
    - 智能驾驶
    - 政策法规
    - 国际车企
    
    2. 提炼“今日核心趋势”（3条）：
    要求：
    - 必须是行业趋势，不是单条新闻
    - 用一句话总结
    - 排序按重要性
    
    3. 输出严格 JSON：
    
    格式如下：
    {{
      "trends": [
        "趋势1",
        "趋势2",
        "趋势3"
      ],
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
