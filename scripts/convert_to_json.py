# scripts/convert_to_json.py
import re
import json
import sys
import os

if len(sys.argv) != 2:
    print("❌ 请提供 .txt 文件路径作为参数")
    sys.exit(1)

txt_path = sys.argv[1]
if not os.path.isfile(txt_path):
    print(f"❌ 文件不存在: {txt_path}")
    sys.exit(1)

with open(txt_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 匹配格式：标题\n来源\n链接\n---
pattern = r'(.*?)\n(.*?)\n(https?://[^\n]+)\n---'
matches = re.findall(pattern, content, re.DOTALL)

news_list = []
for title, source, url in matches:
    news_list.append({
        'title': title.strip(),
        'source': source.strip(),
        'url': url.strip()
    })

print(json.dumps(news_list, ensure_ascii=False, indent=2))
