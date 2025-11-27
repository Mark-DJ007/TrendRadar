import os
import glob

def find_latest_txt_file():
    """
    在 output 目录中查找最新修改的 .txt 文件。
    """
    # 定义要搜索的目录和文件类型
    search_path = os.path.join('output', '**', '*.txt')
    
    # 查找所有匹配的文件
    list_of_files = glob.glob(search_path, recursive=True)
    
    if not list_of_files:
        return None
    
    # 返回最新修改的文件路径
    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file

if __name__ == "__main__":
    latest_file = find_latest_txt_file()
    if latest_file:
        print(latest_file)
    else:
        print("")  # 如果没找到，输出空字符串，这样在外部判断时 if [ -f "$LATEST_TXT" ] 会失败
