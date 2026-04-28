import os
import json
import requests
from datetime import datetime

# =========================
# 1️⃣ 配置
# =========================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("❌ GEMINI_API_KEY 未配置")

MODEL = "gemini-2.5-flash"
CATEGORIES = ["新能源", "智能驾驶", "政策法规", "国际车企"]

# =========================
# 2️⃣ 读取新闻
# =========================

def get_run_date():
    return os.environ.get("RUN_DATE") or datetime.now().strftime("%Y-%m-%d")


def get_output_dir():
    return os.path.join("output", get_run_date())


output_dir = get_output_dir()
news_path = os.path.join(output_dir, "news.json")
structured_path = os.path.join(output_dir, "daily_structured.json")

with open(news_path, "r", encoding="utf-8") as f:
    news_data = json.load(f)

# 🔥 控制规模（非常重要，防止AI崩）
news_data = news_data[:30]

# =========================
# 3️⃣ 构造输入文本（稳定版）
# =========================

news_text = "\n".join(
    f"- {n.get('title','')}：{n.get('summary','')[:200]}"
    for n in news_data
)

# =========================
# 4️⃣ Prompt（稳定JSON输出）
# =========================

prompt = f"""
你是汽车行业分析师。

请严格输出 JSON（不要解释、不要markdown）。

任务：
1. 分类：
- 新能源
- 智能驾驶
- 政策法规
- 国际车企

2. 每类最多5条

3. 提炼3条“今日核心趋势”（行业级，不是单条新闻）

输出必须严格符合：

{{
  "trends": ["", "", ""],
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
# 5️⃣ 调用 Gemini
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

    print("status:", res.status_code)
    print("response:", res.text)   # 🔥关键

    if res.status_code != 200:
        raise Exception("Gemini API failed")

    return res.json()["candidates"][0]["content"]["parts"][0]["text"]
# =========================
# 6️⃣ JSON安全解析
# =========================

def safe_parse(text):
    try:
        return json.loads(text)
    except Exception:
        print("❌ JSON解析失败，尝试截取...")

        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except Exception:
            print("❌ 截取失败，返回兜底结构")
            return {
                "trends": [],
                "新能源": [],
                "智能驾驶": [],
                "政策法规": [],
                "国际车企": []
            }


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


def backfill_links(structured_data, source_news):
    link_map = build_link_map(source_news)
    filled = 0
    missing = 0

    for category in CATEGORIES:
        for item in structured_data.get(category, []):
            current_link = (item.get("link") or "").strip()
            if current_link:
                continue

            matched = link_map.get(_normalize_title(item.get("title", "")), "")
            if matched:
                item["link"] = matched
                filled += 1
            else:
                missing += 1

    print(f"🔗 链接回填: 成功 {filled} 条, 仍缺失 {missing} 条")
    return structured_data


# =========================
# 7️⃣ 主流程
# =========================

result = call_gemini(prompt)

print("===== Gemini 原始输出 =====")
print(result)

result_json = safe_parse(result)
result_json = backfill_links(result_json, news_data)

# =========================
# 8️⃣ 保证字段完整
# =========================

default_keys = ["trends"] + CATEGORIES

for k in default_keys:
    if k not in result_json:
        result_json[k] = []

# =========================
# 9️⃣ 输出文件
# =========================

os.makedirs(output_dir, exist_ok=True)

with open(structured_path, "w", encoding="utf-8") as f:
    json.dump(result_json, f, ensure_ascii=False, indent=2)

print(f"✅ structured JSON 已生成: {structured_path}")