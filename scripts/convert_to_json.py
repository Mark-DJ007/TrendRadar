import json
import sys
import os
import re

def parse_txt_to_json(file_path: str):
    """
    一个以URL为中心的、极度宽容的解析器。
    它不假设任何固定格式，而是在整个文件中智能地寻找标题和URL的配对。
    """
    news_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 核心思路：
        # 1. 先用一个宽松的正则，找出文件里所有看起来像URL的字符串。
        # 2. 对于每一个找到的URL，我们再尝试在它附近寻找一个最合理的标题。

        # 匹配以http开头，不包含空白字符的URL，直到遇到一个非URL字符为止
        url_pattern = re.compile(r'(https?://[^\s\[\]"\'<>]+)')
        
        all_urls = url_pattern.findall(content)

        if not all_urls:
            print("警告: 在文件中没有找到任何符合格式的URL。", file=sys.stderr)
            return []

        # 遍历找到的每一个URL
        for url in all_urls:
            # 在内容中找到这个URL的位置
            url_pos = content.find(url)
            if url_pos == -1:
                continue

            # 提取URL所在的行及其前后文，用于寻找标题
            # 我们定义一个“上下文窗口”，比如URL前后各200个字符
            start = max(0, url_pos - 200)
            end = min(len(content), url_pos + 200)
            context = content[start:end]

            # --- 标题提取策略 ---
            # 策略1: 尝试从上下文中找到 "URL:" 标签，并获取它前面的文本作为标题
            title_match = re.search(r'(.*?)\s*(?:\[ur[^\]]*\]|\bURL:)', context, re.IGNORECASE | re.DOTALL)
            
            # 策略2: 如果没找到，尝试找到URL前的换行符，然后取换行符到URL之间的文本
            if not title_match:
                title_match = re.search(r'(.*?)\s*%s' % re.escape(url), context, re.DOTALL)

            # 策略3: 如果还是没找到，就直接使用整个上下文
            if not title_match:
                potential_title = context.strip()
            else:
                potential_title = title_match.group(1).strip()

            # --- 最终数据清洗 ---
            title = potential_title.strip(' "\'。,!?.')
            url = url.strip()

            # 清理标题中的噪音，比如“1. ”、“【】”等
            title = re.sub(r'^\d+[\.\)]\s*', '', title) # 移除开头的数字序号
            title = re.sub(r'^[【\[][^】\]]*[】\]]\s*', '', title) # 移除开头的【xxx】标签

            # 确保标题和URL都不为空，且标题长度大于5（避免抓取到无意义短语）
            if title and url and url.lower().startswith('http') and len(title) > 5:
                # 去重，避免同一个URL被添加多次
                if not any(item['url'] == url for item in news_list):
                    news_list.append({"title": title, "url": url})
        
        return news_list

    except Exception as e:
        print(f"解析文件时发生严重错误: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python convert_to_json.py <path_to_txt_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.isfile(input_file):
        print(f"错误: 文件不存在 {input_file}", file=sys.stderr)
        sys.exit(1)
        
    output_json = parse_txt_to_json(input_file)
    
    # 使用 json.dumps 来确保生成的JSON是严格格式化的
    print(json.dumps(output_json, ensure_ascii=False, indent=2))
