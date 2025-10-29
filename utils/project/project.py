import copy
import os
import re
import shutil
import sys
import winreg as reg
import psutil

from configs.Config import Config
# from evaluation.utiles import global_data



class project:
    global local_path
    local_path = ''
    global data_path
    data_path = 'D:/Pure'
    global path_map
    path_map = {
        'user': '/user.sepc',
        'project': 'sepflow_project',
        'project_configs': '/configs.sepc',
        'global_params': '/global.sepc',
        'global_db': '/global_db.sepc',
        'bufferpro': '/bufferpro.sepc',
        'users': '/users.sepc',
        'global_params_default': '/global.sepc',
        'language': '/global.sepc',
        'license': '/license.sepc',
        'curves_params': '/curves.sepc',
        'curves_params_default': '/curves.sepc',
        'curves_table': '/curves.sepc',
        'analysis_params': '/analysis.sepc',
        'analysis_params_default': '/analysis.sepc',
        'calibration_params': '/calibration.sepc',
        'device_params': '/configs.sepc',
        'equipment': '/configs.sepc',
        'cond_demarcate': '/cond_demarcate.csv',
        'ph_demarcate': '/ph_demarcate.csv',
        'parameters': '/parameters.db'
    }
    global path_suffix
    path_suffix = '/extra-data'
    global path_default
    path_default = '/default'
    global path_welcome  # welcome.exe 应该没有作用
    path_welcome = '/welcome.exe'

    # 检查项目路径并确保所有必要的目录和文件都存在。如果某些配置文件或目录不存在，则尝试从指定的源目录复制它们。此外，还会创建数据、报告和快照等目录
    @staticmethod
    def checkPath():
        project.setLocalPath()
        project_path = project.getRootPath()
        sources = copy.copy(local_path)

        print('project_path--->', local_path)
        if not os.path.exists(project_path):

            project.copyProjectFiles(sources + path_suffix, project_path + path_suffix)

        else:
            for item in path_map:
                exist = True if os.path.exists(project_path + path_suffix + path_map[item]) else False
                try:
                    if not exist:
                        print('Some configs is not exist!Please check your folders!')
                        pass
                except Exception as e:

                    print(e)
        # if not
        data_folder = project.getDataFolder()
        report_folder = project.getReportFolder()
        snapshot_folder = project.getSnapshotFolder()
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        os.popen('attrib +s +a +h +r {}'.format(data_folder))
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        if not os.path.exists(snapshot_folder):
            os.makedirs(snapshot_folder)
        # if not os.path.exists(tmp_folder):
        #     os.makedirs(tmp_folder)
        method_folder = project.getMethodFolder()
        log_folder = project.getLogFolder()
        buffer_folder = project.getBufferFolder()
        project.checkFolder(method_folder, '/method')
        project.checkFolder(log_folder, '/log')
        project.checkFolder(buffer_folder, '/buffer')

    # 当打包为生产版本时，用于检查路径的辅助方法。
    @staticmethod
    def checkPath2():

        project.setLocalPath()
        if getattr(sys, 'frozen', False):
            project.getRootPath()
            # 检查extra-data是否存在
            project.checkExtraData()

            project.checkLogFolder()

        # 临时添加
        signature = r'D:\Pure\extra-data\evaluation\signature'
        if not os.path.exists(signature):
            os.makedirs(signature)

        current = r'D:\Pure\extra-data\evaluation\current'
        if not os.path.exists(current):
            os.makedirs(current)

        from evaluation.utiles import global_data

        global_data.res = copy.copy(project.getRootPath() + path_suffix + '/evaluation/res/')



    @staticmethod
    def check_project_path(project_name):


        Config.set_data('project_name',project_name)
        if getattr(sys, 'frozen', False):
            project.checkDataFolder()
            project.checkOtherFolder()

        elif __file__:
            project.checkOtherFolder()


    @staticmethod
    def checkDataFolder():
        data_folder = project.getDataFolder() + '/demo_data'
        is_need = os.path.exists(data_folder)
        project.checkFolder2(data_folder)
        source_target = local_path + path_suffix + '/demo_data'
        if not is_need:
            os.popen(r'xcopy "{}" "{}" /s/y/e'.format(r'{}'.format(source_target), r'{}'.format(data_folder)))
        os.popen('attrib +s +a +h +r {}'.format(data_folder))

    @staticmethod
    def checkOtherFolder():
        report_folder = project.getReportFolder()
        snapshot_folder = project.getSnapshotFolder()
        method_folder = project.getMethodFolder()
        method_queue_folder = project.getMethodQueueFolder()
        buffer_folder = project.getBufferFolder()
        manual_folder = project.getManualFolder()
        phase_folder = project.getMethodPhaseFolder()
        project.checkFolder2(report_folder)
        project.checkFolder2(snapshot_folder)
        project.checkFolder2(method_folder)
        project.checkFolder2(method_queue_folder)
        project.checkFolder2(buffer_folder)
        project.checkFolder2(manual_folder)
        project.checkFolder2(phase_folder)

    @staticmethod
    def copy_and_override_files(source_path, target_path):
        # 遍历源目录
        for root, dirs, files in os.walk(source_path):
            for file in files:
                # 计算源文件和目标文件的完整路径
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_path)
                target_file_path = os.path.join(target_path, relative_path, file)
                # 确保目标目录存在
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                # 如果文件名是 "license.spec"，检查目标路径是否已存在此文件
                if file in ['license.sepc', 'software_config.json'] and os.path.exists(target_path + '/license.sepc'):
                    continue  # 如果目标路径已存在 "license.spec"，则跳过复制
                # 复制文件，如果文件已存在，则覆盖
                shutil.copy2(source_file_path, target_file_path)

    @staticmethod
    def set_registry_key(key_path, value_name):

        value_data = 1

        # 判断指定的注册表值是否存在
        def reg_value_exists(root, subkey, val_name):
            try:
                key = reg.OpenKey(root, subkey, 0, reg.KEY_READ)
                reg.QueryValueEx(key, val_name)
                reg.CloseKey(key)
                return True
            except (FileNotFoundError, OSError):
                return False

        # 创建或修改注册表项
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE | reg.KEY_CREATE_SUB_KEY)
        except FileNotFoundError:
            key = reg.CreateKey(reg.HKEY_CURRENT_USER, key_path)

        if not reg_value_exists(reg.HKEY_CURRENT_USER, key_path, value_name):
            try:
                reg.SetValueEx(key, value_name, 0, reg.REG_DWORD, value_data)
            except PermissionError as e:
                print(f"PermissionError: {e}. Make sure you have enough permissions.")
            finally:
                reg.CloseKey(key)
        else:
            reg.CloseKey(key)

    # 检查额外数据目录是否存在，如果不存在，从指定源复制。
    @staticmethod
    def checkExtraData():
        key_path = r"Software\ChromX"
        value_name = "isFirstRun"
        project.set_registry_key(key_path, value_name)

        extra_data = project.getRootPath() + path_suffix
        source_target = local_path + path_suffix
        try:
            # 打开注册表项以读取 isFirstRun 值
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_READ | reg.KEY_SET_VALUE) as key:
                value, _ = reg.QueryValueEx(key, value_name)
                if value:
                    print('First run!!')
                    # project.copy_and_override_files(source_target, extra_data)
                    reg.SetValueEx(key, "isFirstRun", 0, reg.REG_DWORD, 0)
                else:
                    print('no first run!!')
                if not os.path.exists(extra_data):
                    project.copyProjectFiles(source_target, extra_data)
                os.popen('attrib -r {}/*.* /s'.format(extra_data))
        except:
            print("checkExtraData Error")

    @staticmethod
    def checkLogFolder():
        log_file = 'log.sepd'
        log_folder = project.getRootPath() + '/log'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        target_log_path = project.getRootPath() + '/log/' + log_file
        print('target log file-->', target_log_path)
        if not os.path.exists(target_log_path):
            source_log_path = local_path + path_suffix + '/' + 'log.sepd.clear'
            print('source log path-->', source_log_path)
            try:
                shutil.copy(source_log_path, target_log_path)
            except Exception as e:
                print("Unable to copy file. %s" % e)
                print(e)
        os.popen('attrib -r {}'.format(target_log_path))
        pass

    # 检查给定文件夹是否存在，如果不存在，则尝试从项目根目录移动或创建新的文件夹。
    @staticmethod
    def checkFolder(folder_name, folder_type):
        if os.path.exists(folder_name):
            return True
        else:
            if os.path.exists(project.getRootPath() + path_suffix + folder_type):
                shutil.move(project.getRootPath() + path_suffix + folder_type, folder_name)
            else:
                os.makedirs(folder_name)
        pass

    # 确保指定的文件夹存在，如果不存在，则创建。
    @staticmethod
    def checkFolder2(folder):
        if not os.path.exists(folder):
            os.makedirs(folder)


    @staticmethod
    def getRootPath():
        if getattr(sys, 'frozen', False):
            global data_path
            data_path = data_path.replace('\\\\', '/').replace('\\', '/')
            return copy.copy(data_path)
        elif __file__:
            return copy.copy(local_path)
        pass

    @staticmethod
    def getPath_suffix():
        return path_suffix



    @staticmethod
    def setLocalPath():
        global local_path
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            rootPath = application_path
        elif __file__:
            application_path = os.path.dirname(os.path.abspath(__file__))
            rootPath = application_path[:application_path.find(path_map['project']) + len(path_map['project'])]
        local_path = rootPath.replace('\\\\', '/').replace('\\', '/')
        pass

    @staticmethod
    def getConfigPath(types, isDefault=False):
        if isDefault:
            return copy.copy(project.getRootPath() + path_suffix + path_default + path_map[types])
        else:
            return copy.copy(project.getRootPath() + path_suffix + path_map[types])

    @staticmethod
    def getDataFolder():
        return project.getDataFileFolder('Data')

    @staticmethod
    def getReportFolder():
        return project.getDataFileFolder('report')

    # 快照保存的路径
    @staticmethod
    def getSnapshotFolder():
        return project.getDataFileFolder('snapshot')

    @staticmethod
    def getLogFolder():
        return project.getDataFileFolder('log')

    @staticmethod
    def getLogFile():
        return project.getDataFileFolder('log') + '/log.sepd'

    @staticmethod
    def getLanguagePath(file):
        return local_path + path_suffix + '/lan/' + file


    # 获取预装柱的路径
    @staticmethod
    def get_column():
        column_db_path = project.getRootPath() + path_suffix + '/column/column.db'
        return column_db_path

    # 曲线的路径
    @staticmethod
    def get_curve_path():
        return project.getRootPath() + path_suffix + '/curves.sepc'


    @staticmethod
    def getDataFileFolder(file_type):
        project_name = Config.get_data('project_name')
        if file_type == 'log':
            if getattr(sys, 'frozen', False):
                return copy.copy(project.getRootPath() + '/{}'.format(file_type))
            elif __file__:
                return copy.copy(project.getRootPath() + '/project/{}'.format(file_type))
        else:
            if getattr(sys, 'frozen', False):
                return copy.copy(project.getRootPath() + '/project/{}/{}'.format(project_name,file_type))
            elif __file__:
                return copy.copy(project.getRootPath() + '/project/{}/{}'.format(project_name,file_type))

    @staticmethod
    def get_project_path():
        project_name = Config.get_data('project_name')
        path = copy.copy(project.getRootPath() + '/project/{}'.format(project_name))
        return path



    @staticmethod
    def getTmpFolder():
        return project.getDataFileFolder('tmp')

    @staticmethod
    def getResFolder():
        return copy.copy(local_path + path_suffix + '/res')

    @staticmethod
    def get_evaluation_folder():
        return copy.copy(project.getRootPath() + path_suffix + '/evaluation/')



    @staticmethod
    def getMethodFolder():
        return project.getDataFileFolder('method')

    @staticmethod
    def getManualFolder():
        return project.getDataFileFolder('manual')

    @staticmethod
    def getMethodQueueFolder():
        return project.getDataFileFolder('method_queue')

    @staticmethod
    def getBufferFolder():
        return project.getDataFileFolder('buffer')

    @staticmethod
    def getMethodTplFolder():
        return project.getDataFileFolder('method') + '/template'


    @staticmethod
    def getMethodPhaseFolder():
        return project.getDataFileFolder('phase')

    @staticmethod
    def copyProjectFiles(source, target):
        try:
            shutil.copytree(source, target)
        except Exception as e:
            pass

