import json
import sys
import os
import re
 
def parse_txt_to_json(file_path: str):
    """
    一个极度健壮的解析器，用于处理格式混乱、有拼写错误的TrendRadar TXT文件。
    它能处理URL中的换行符和常见的URL标签拼写错误。
    """
    news_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
 
        # 核心改进：先按行读取，然后把属于同一条新闻的行合并起来
        # 这样可以解决URL被换行符切断的问题
        raw_lines = content.split('\n')
        merged_lines = []
        buffer = ""
        for line in raw_lines:
            line = line.strip()
            if not line:
                if buffer:
                    merged_lines.append(buffer)
                    buffer = ""
                continue
            
            # 如果一行以数字开头，说明是新的一条新闻
            if re.match(r'^\d+\.', line):
                if buffer:
                    merged_lines.append(buffer)
                buffer = line
            else:
                # 否则，这是上一行的延续，合并它们
                buffer += " " + line
        
        if buffer:
            merged_lines.append(buffer)
 
        # 现在处理合并后的、干净的行
        for line in merged_lines:
            # 使用更宽松的匹配，只要包含 [ur 就认为是URL标签，可以匹配 [URL:, [ur1:, [UrL: 等
            if "[ur" in line:
                
                # 提取标题: 从行首数字后，到 [ur 之前
                title_match = re.search(r'^\d+\.\s*(.*?)\s*\[ur', line, re.IGNORECASE)
                if not title_match:
                    continue
                title = title_match.group(1).strip()
 
                # 提取URL: 从 [ur 到 ] 之间
                url_match = re.search(r'\[ur(.*?)\]', line, re.IGNORECASE)
                if not url_match:
                    continue
                url = url_match.group(1).strip()
                
                # 最终数据清洗
                title = title.strip(' "\'')
                # 移除URL中可能存在的所有空白符（包括换行、空格、制表符）
                url = re.sub(r'\s+', '', url)
 
                # 确保标题和URL都不为空，且URL有效
                if title and url and url.lower().startswith('http'):
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
 
