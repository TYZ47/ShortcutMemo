import os
import sys


class Project:
    """项目路径管理类"""

    path_map = {
        'data': 'config/data.db',
    }
    
    @staticmethod
    def get_project_path():
        """
        获取软件开始运行的目录（项目根目录）
        无论project.py在哪里，都能找到实际运行main.py的目录
        
        Returns:
            str: 项目根目录路径
        """
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            return os.path.dirname(sys.executable)
        else:
            # 获取实际运行的脚本路径（通常是main.py）
            main_script = sys.argv[0]
            if os.path.isfile(main_script):
                # 如果是文件，获取其所在目录
                script_dir = os.path.dirname(os.path.abspath(main_script))
                # 检查该目录是否有main.py
                if os.path.exists(os.path.join(script_dir, 'main.py')):
                    return script_dir
                # 如果没有，尝试向上查找包含main.py的目录
                current = script_dir
                while current != os.path.dirname(current):  # 直到根目录
                    if os.path.exists(os.path.join(current, 'main.py')):
                        return current
                    current = os.path.dirname(current)
            else:
                # 如果sys.argv[0]不是文件，可能是模块运行
                # 从当前工作目录开始查找
                current = os.getcwd()
                while current != os.path.dirname(current):  # 直到根目录
                    if os.path.exists(os.path.join(current, 'main.py')):
                        return current
                    current = os.path.dirname(current)
            
            # 如果都没找到，返回当前工作目录作为备选
            return os.getcwd()
    

    @staticmethod
    def get_path(key):
        """
        根据key获取对应的路径
        
        Args:
            key: 路径映射的key
            
        Returns:
            str: 完整路径
        """
        return os.path.join(Project.get_project_path(), Project.path_map[key])