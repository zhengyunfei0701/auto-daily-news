import os
import json
import requests

# =========================
# 1️⃣ 配置
# =========================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("❌ GEMINI_API_KEY 未配置")

MODEL = "gemini-2.5-flash"

# =========================
# 2️⃣ 读取新闻
# =========================

with open("output/news.txt", "r", encoding="utf-8") as f:
    news_text = f.read()

# =========================
# 3️⃣ Prompt（强约束 JSON）
# =========================

prompt = f"""
你是汽车行业分析师。

请对以下新闻进行分析，并严格输出 JSON（非常重要，不能多任何字符）。

要求：

1. 分类：
- 新能源
- 智能驾驶
- 政策法规
- 国际车企

2. 每类最多5条新闻（按重要性排序）

3. 提炼3条“今日核心趋势”（必须是行业趋势，不是单条新闻）

4. 输出必须是合法 JSON，不能有 markdown、不能有解释

JSON格式如下：

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
{news_text}
"""

# =========================
# 4️⃣ 调用 Gemini
# =========================

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    res = requests.post(url, json=payload)

    if res.status_code != 200:
        print("❌ API错误：")
        print(res.text)
        raise Exception("Gemini API failed")

    return res.json()["candidates"][0]["content"]["parts"][0]["text"]


# =========================
# 5️⃣ 主流程
# =========================

result = call_gemini(prompt)

print("===== Gemini 原始输出 =====")
print(result)

# =========================
# 6️⃣ 强制 JSON 解析（关键稳定点）
# =========================

def safe_parse(text):
    try:
        return json.loads(text)
    except Exception as e:
        print("❌ JSON解析失败，进入兜底模式")

        # 尝试截取 JSON（防止AI多输出）
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except:
            print("❌ 截取后仍失败，返回空结构")
            return {
                "trends": [],
                "新能源": [],
                "智能驾驶": [],
                "政策法规": [],
                "国际车企": []
            }


result_json = safe_parse(result)

# =========================
# 7️⃣ 保证字段完整（防崩）
# =========================

default_keys = ["trends", "新能源", "智能驾驶", "政策法规", "国际车企"]

for k in default_keys:
    if k not in result_json:
        result_json[k] = []

# =========================
# 8️⃣ 输出目录保证存在
# =========================

os.makedirs("output", exist_ok=True)

with open("output/daily_structured.json", "w", encoding="utf-8") as f:
    json.dump(result_json, f, ensure_ascii=False, indent=2)

print("✅ structured JSON 已生成")
