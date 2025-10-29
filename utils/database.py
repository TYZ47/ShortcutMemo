from PyQt5.QtCore import QObject, QMutex
import os
import sqlite3
import json
import warnings

from utils import Project

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Database(QObject):
    _instance = None
    _lock = QMutex()

    def __new__(cls):
        if cls._instance is None:
            cls._lock.lock()
            try:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
            finally:
                cls._lock.unlock()
        return cls._instance

    def __init__(self):
        super().__init__()
        if hasattr(self, '_initialized'):
            return

        # 按需求设置类变量
        self.path = Project.get_path('data')  # 实际是sqlite3类型
        self.lock = QMutex()



        self._initialized = True
        self.init_db()

    @classmethod
    def getInstance(cls):

        return cls()

    def init_db(self):
        """初始化数据库，如果数据库不存在则创建"""
        # 获取数据库文件路径
        db_dir = os.path.dirname(self.path)
        
        # 如果目录不存在，创建目录
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # 检查数据库文件是否存在
        db_exists = os.path.exists(self.path)
        
        # 连接数据库
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        
        try:
            # 创建基础表结构
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shortcuts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    shortcut TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            
            if not db_exists:
                print(f"数据库已创建: {self.path}")
            else:
                print(f"数据库已存在: {self.path}")
                
        except Exception as e:
            print(f"初始化数据库时出错: {e}")
        finally:
            cursor.close()
            conn.close()




