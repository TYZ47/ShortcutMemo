import os
import sys


class Project:

    path_map = {
        'data': 'config/data.db',
    }
    
    @staticmethod
    def get_project_path():
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            return os.path.dirname(sys.executable)
        else:
            # 获取当前文件所在目录（utils目录）
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上查找一级，找到项目根目录
            project_root = os.path.dirname(current_dir)
            return project_root
    

    @staticmethod
    def get_path(key):

        return os.path.join(Project.get_project_path(), Project.path_map[key])