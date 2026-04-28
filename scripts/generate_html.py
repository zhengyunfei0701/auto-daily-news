import os
import re
from datetime import datetime


def get_run_date():
    return os.environ.get("RUN_DATE") or datetime.now().strftime("%Y-%m-%d")


def get_output_dir():
    return os.path.join("output", get_run_date())


def escape_html(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def convert_inline_markdown(line):
    line = escape_html(line)
    line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
    line = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', line)
    return line


def markdown_to_html(md_text):
    html_parts = []
    in_ol = False

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            continue

        if stripped == "---":
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            html_parts.append('<hr class="divider" />')
            continue

        if stripped.startswith("# "):
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            html_parts.append(f"<h1>{convert_inline_markdown(stripped[2:])}</h1>")
            continue

        if stripped.startswith("## "):
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            html_parts.append(f"<h2>{convert_inline_markdown(stripped[3:])}</h2>")
            continue

        ordered_match = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if ordered_match:
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            html_parts.append(f"<li>{convert_inline_markdown(ordered_match.group(2))}</li>")
            continue

        if in_ol:
            html_parts.append("</ol>")
            in_ol = False
        html_parts.append(f"<p>{convert_inline_markdown(stripped)}</p>")

    if in_ol:
        html_parts.append("</ol>")

    return "\n".join(html_parts)


def build_html_page(content_html, run_date):
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>汽车行业日报 {run_date}</title>
  <style>
    body {{
      margin: 0;
      background: #f5f7fb;
      color: #1f2937;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.7;
    }}
    .page {{
      max-width: 760px;
      margin: 0 auto;
      padding: 14px 12px 28px;
    }}
    .article {{
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 14px 12px;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 22px;
      color: #111827;
    }}
    h2 {{
      margin: 18px 0 8px;
      font-size: 18px;
      color: #111827;
    }}
    p {{
      margin: 8px 0;
      font-size: 15px;
      color: #374151;
    }}
    ol {{
      margin: 8px 0 12px;
      padding-left: 20px;
    }}
    li {{
      margin: 6px 0;
      font-size: 15px;
      color: #374151;
    }}
    .divider {{
      border: none;
      border-top: 1px dashed #d1d5db;
      margin: 14px 0;
    }}
    a {{
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <main class="page">
    <article class="article">
      {content_html}
    </article>
  </main>
</body>
</html>"""


if __name__ == "__main__":
    run_date = get_run_date()
    output_dir = get_output_dir()
    md_path = os.path.join(output_dir, "daily.md")
    html_path = os.path.join(output_dir, "daily.html")

    if not os.path.exists(md_path):
        print(f"❌ md 文件不存在，跳过 HTML 生成: {md_path}")
        raise SystemExit(0)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    content_html = markdown_to_html(md_text)
    html = build_html_page(content_html, run_date)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML 已生成: {html_path}")