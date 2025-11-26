import json
import sys
import os
import re
 
def parse_txt_to_json(file_path: str):
    """
    解析 TrendRadar main.py 生成的TXT文件，转换为JSON列表。
    期望的格式：
    source_id
    1. title [URL:url] [MOBILE:mobile_url]
    2. title [URL:url]
    ...
    """
    news_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 这个正则表达式更健壮，能正确处理带引号的标题
        # 它会捕获排名之后、[URL:之前的所有内容作为标题
        line_pattern = re.compile(
            r'^\d+\.\s*(.*?)\s*\[URL:(.*?)\]'
 
        )
 
        for line in lines:
            line = line.strip()
            # 我们只处理包含 "[URL:" 的行，这通常是新闻条目
            if "[URL:" in line:
                match = line_pattern.match(line)
                if match:
                    title = match.group(1).strip()
                    url = match.group(2).strip()
                    
                    # 再次清理标题，移除可能残留的引号和多余空格
                    title = title.strip(' "\'')
                    
                    # 确保标题和URL都不为空，并且URL看起来像个URL
                    if title and url and url.startswith('http'):
                        news_list.append({"title": title, "url": url})
        
        return news_list
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"解析文件时出错: {e}", file=sys.stderr)
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
    
    # 将结果以JSON格式打印到标准输出
    # 使用 json.dumps 来确保生成的JSON是严格格式化的，没有语法错误
    print(json.dumps(output_json, ensure_ascii=False, indent=2))
 
