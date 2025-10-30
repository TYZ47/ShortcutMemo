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
            # 创建软件表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS software (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            ''')

            # 创建快捷键表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shortcut (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    software_id INTEGER NOT NULL,
                    function TEXT NOT NULL,
                    keys TEXT NOT NULL,
                    note TEXT,
                    FOREIGN KEY (software_id) REFERENCES software (id)
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

    def get_name_list(self):

        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT name FROM software ORDER BY id")
                results = cursor.fetchall()
                # 返回名称列表（去掉元组包装）
                return [row[0] for row in results]
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"获取软件名称列表时出错: {e}")
            return []
        finally:
            self.lock.unlock()

    def insert_name(self, name):

        if not name or not name.strip():
            print("软件名称不能为空")
            return False

        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                # 检查是否已存在相同的名称
                cursor.execute(
                    "SELECT id FROM software WHERE name = ?", (name.strip(),))
                if cursor.fetchone():
                    print(f"软件名称 '{name}' 已存在")
                    return False

                # 插入新名称
                cursor.execute(
                    "INSERT INTO software (name) VALUES (?)", (name.strip(),))
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                print(f"插入软件名称时出错: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        finally:
            self.lock.unlock()

    def delete_name(self, name):

        if not name or not name.strip():
            print("软件名称不能为空")
            return False
        
        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                # 首先查找软件ID
                cursor.execute("SELECT id FROM software WHERE name = ?", (name.strip(),))
                result = cursor.fetchone()
                
                if not result:
                    print(f"软件 '{name}' 不存在")
                    return False
                
                software_id = result[0]
                
                # 删除相关的快捷键记录
                cursor.execute("DELETE FROM shortcut WHERE software_id = ?", (software_id,))
                deleted_shortcuts = cursor.rowcount
                
                # 删除软件记录
                cursor.execute("DELETE FROM software WHERE id = ?", (software_id,))
                deleted_software = cursor.rowcount
                
                conn.commit()
                
                if deleted_software > 0:
                    print(f"成功删除软件 '{name}' 及其 {deleted_shortcuts} 条快捷键记录")
                    return True
                else:
                    print(f"删除软件 '{name}' 失败")
                    return False
                    
            except Exception as e:
                conn.rollback()
                print(f"删除软件时出错: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        finally:
            self.lock.unlock()

    def get_id_by_name(self, name):

        if not name or not name.strip():
            print("软件名称不能为空")
            return None
        
        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id FROM software WHERE name = ?", (name.strip(),))
                result = cursor.fetchone()
                
                if result:
                    return result[0]
                else:
                    return None
            except Exception as e:
                print(f"根据名称查找ID时出错: {e}")
                return None
            finally:
                cursor.close()
                conn.close()
        finally:
            self.lock.unlock()
    
    def get_shortcut_info_by_id(self, software_id):
        """
        根据软件ID获取快捷键信息
        
        Args:
            software_id: 软件ID
            
        Returns:
            list: 包含(function, keys, note)元组的列表
        """
        if not software_id:
            print("软件ID不能为空")
            return []
        
        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT function, keys, note 
                    FROM shortcut 
                    WHERE software_id = ? 
                    ORDER BY id
                """, (software_id,))
                
                results = cursor.fetchall()
                return results
            except Exception as e:
                print(f"根据软件ID获取快捷键信息时出错: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
        finally:
            self.lock.unlock()

    def insert_shortcut(self, software_id, function, shortcut, note):

        if not software_id:
            print("软件ID不能为空")
            return False
        
        if not function or not function.strip():
            print("功能名称不能为空")
            return False
        
        if not shortcut or not shortcut.strip():
            print("快捷键不能为空")
            return False
        
        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                # 检查是否已存在相同的快捷键
                cursor.execute("""
                    SELECT id FROM shortcut 
                    WHERE software_id = ? AND function = ? AND keys = ?
                """, (software_id, function.strip(), shortcut.strip()))
                
                if cursor.fetchone():
                    print(f"快捷键 '{function} - {shortcut}' 已存在")
                    return False
                
                # 插入新快捷键
                cursor.execute("""
                    INSERT INTO shortcut (software_id, function, keys, note) 
                    VALUES (?, ?, ?, ?)
                """, (software_id, function.strip(), shortcut.strip(), note.strip() if note else ""))
                conn.commit()
                print(f"成功添加快捷键: {function} - {shortcut}")
                return True
            except Exception as e:
                conn.rollback()
                print(f"添加快捷键时出错: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        finally:
            self.lock.unlock()

    def get_shortcut_name_by_id(self, software_id: int) -> list:
        """根据软件ID获取快捷键名称列表"""
        if not software_id:
            return []
        
        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT function FROM shortcut WHERE software_id = ?", (software_id,))
                return [row[0] for row in cursor.fetchall()]
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            print(f"获取快捷键名称列表时出错: {e}")
            return []
        finally:
            self.lock.unlock()
    
    def delete_shortcut(self, software_id, function):
        """删除指定的快捷键"""
        if not software_id or not function:
            return False
        
        self.lock.lock()
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM shortcut WHERE software_id = ? AND function = ?", (software_id, function))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                conn.rollback()
                print(f"删除快捷键时出错: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
        finally:
            self.lock.unlock()