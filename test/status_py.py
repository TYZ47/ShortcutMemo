# todo 输入路径，然后找到这个路径下的所有py文件，然后打印出来，文件夹下面的文件也要考虑
# todo，统计所有py代码的行数

from pathlib import Path


def find_py_files(directory_path):
    """
    查找指定路径下所有py文件（包括子文件夹）
    
    Args:
        directory_path: 要搜索的目录路径
        
    Returns:
        list: 所有找到的py文件路径列表
    """
    path = Path(directory_path)
    if not path.exists():
        print(f"错误：路径 '{directory_path}' 不存在")
        return []
    
    py_files = []
    for py_file in path.rglob("*.py"):
        py_files.append(py_file)
    
    return py_files


def count_lines(file_path):
    """
    统计文件的行数
    
    Args:
        file_path: 文件路径
        
    Returns:
        int: 文件行数
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception as e:
        print(f"读取文件 '{file_path}' 时出错：{e}")
        return 0


def main():
    my_path = r"D:\Code\ShortcutMemo"
    
    # 查找所有py文件
    py_files = find_py_files(my_path)
    
    if not py_files:
        print(f"在路径 '{my_path}' 下未找到任何 .py 文件")
        return
    
    # print(f"在路径 '{my_path}' 下共找到 {len(py_files)} 个 .py 文件：\n")
    # print("=" * 80)
    
    total_lines = 0
    for py_file in sorted(py_files):
        lines = count_lines(py_file)
        total_lines += lines
        # 显示相对路径，更易读
        try:
            relative_path = py_file.relative_to(my_path)
            # print(f"{relative_path}: {lines} 行")
        except:
            print(f"{py_file}: {lines} 行")
    
    # print("=" * 80)
    # print(f"\n总计：{len(py_files)} 个文件，{total_lines} 行代码")
    addlines = total_lines - 747-405
    print(f"新增：{addlines} 行代码")


if __name__ == "__main__":
    main()