import sys
import json

try:
    data = json.load(sys.stdin)
    print(data.get('html_url', '未知'))
except Exception as e:
    print(f"解析失败: {str(e)}")
    sys.exit(1)
