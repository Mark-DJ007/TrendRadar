import os
import sys
from pathlib import Path
 
def find_latest_txt():
    """
    查找 'output' 目录下最新的 .txt 文件并打印其路径。
    如果找不到文件，则向标准错误输出打印信息。
    """
    try:
        # 从'output'目录开始递归查找所有.txt文件
        txt_files = list(Path("output").rglob("*.txt"))
        
        if not txt_files:
            print("NOT_FOUND", file=sys.stderr)
            return None
 
        # 找到最新修改时间的文件
        latest_file = max(txt_files, key=lambda p: p.stat().st_mtime)
        
        # 打印文件路径
        print(latest_file)
        return latest_file
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None
 
if __name__ == "__main__":
    find_latest_txt()
