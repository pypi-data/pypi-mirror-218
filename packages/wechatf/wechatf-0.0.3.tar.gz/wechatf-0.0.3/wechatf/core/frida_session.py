"""
版本判断、建立frida连接、断开连接、加载js脚本
"""
import os
import time
import winreg
import subprocess

import frida
import win32api
import pefile

from . import conf


class FridaSession:
    def __init__(self):
        # 微信主程序名称
        self.wechat_bin_name = "WeChat.exe"

        # 微信主动态链接库名称
        self.wechatwin_dll_name = "WeChatWin.dll"

        # 获取微信版本号
        self.wechatwin_dll_version = self._get_wechatwin_dll_version()
        # 微信架构
        self.wechatwin_dll_arch = self._get_wechatwin_dll_arch()

        # 当前微信版本签名
        self.current_version = f"v{self.wechatwin_dll_version.replace('.', '_')}_{self.wechatwin_dll_arch}"

        # 判断是否支持当前版本
        if self.current_version not in conf.support_version:
            raise Exception(f"不支持当前版本：{self.current_version}")

        print(f"当前微信版本：{self.current_version}")

        # 连接到微信
        self.session = self._get_session()

    def _get_wechat_inst_dir(self):
        """
        获取微信安装目录
        """
        # 定义常量
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
        KEY_READ = winreg.KEY_READ
        REG_PATH = r"SOFTWARE\Tencent\WeChat"

        # 读取注册表中微信安装目录
        try:
            reg_key = winreg.OpenKey(HKEY_CURRENT_USER, REG_PATH, 0, KEY_READ)
            install_dir = winreg.QueryValueEx(reg_key, "InstallPath")[0]
            winreg.CloseKey(reg_key)
        except WindowsError:
            raise Exception("微信未安装或注册表中未找到微信安装路径。")

        return install_dir

    def _get_wechatwin_dll_path(self):
        """
        获取WeChatWin.dll 文件路径
        :return:
        """
        # 获取安装目录
        install_dir = self._get_wechat_inst_dir()
        # print(install_dir)
        dll_path = None
        # 寻找wechatwind.ll文件
        for root, dirs, files in os.walk(install_dir, topdown=False):
            for _file in files:
                # 判断是否相同
                if _file.lower() == self.wechatwin_dll_name.lower():
                    dll_path = os.path.join(install_dir, root, _file)
        return dll_path

    def _get_wechatwin_dll_version(self):
        """
        获取微信版本号
        """
        dll_path = self._get_wechatwin_dll_path()

        # 获取dll文件版本号
        if os.path.isfile(dll_path):
            version_info = win32api.GetFileVersionInfo(dll_path, "\\")
            fixed_info = version_info['FileVersionMS'], version_info['FileVersionLS']
            version = f"{fixed_info[0] >> 16}.{fixed_info[0] & 0xffff}.{fixed_info[1] >> 16}.{fixed_info[1] & 0xffff}"
            # print(f"WeChatWin.dll 版本号：{version}")
            return version
        else:
            raise Exception("未找到 wechatwin.dll 文件。")

    def _get_wechatwin_dll_arch(self):
        """
        获取wechatwin.dll架构
        :return:
        """
        dll_path = self._get_wechatwin_dll_path()

        # 获取dll架构
        try:
            pe = pefile.PE(dll_path, fast_load=True)

            # 获取 PE 文件的机器架构信息
            machine = pe.FILE_HEADER.Machine

            # 根据机器架构信息判断支持的 CPU 架构
            if machine == 0x14C:
                return 'x86'
            elif machine == 0x8664:
                return 'x64'
            else:
                return 'Unknown'
        except Exception as e:
            print(f"Error occurred while opening and analyzing PE file: {e}")
            return 'Unknown'

    def _get_session(self):
        """
        尝试连接到微信
        """
        # 获取设备
        device = frida.get_local_device()

        # 查找微信PID
        pids = device.enumerate_processes()
        wechat_pids = [pid for pid in pids if self.wechat_bin_name.lower() == pid.name.lower()]

        # 如果找到微信进程，则使用第一个进程ID连接到微信
        if wechat_pids:
            pid = wechat_pids[0].pid
        else:
            print('微信未启动，尝试打开微信。')

            # 微信主程序路径
            wechat_bin = os.path.join(self._get_wechat_inst_dir(), self.wechat_bin_name)

            # 启动
            process = subprocess.Popen(wechat_bin)

            # 等待5s
            time.sleep(5)

            # 设置pid
            pid = process.pid

        # 附加到进程
        _session = device.attach(pid)
        print(f'已附加到WeChat.exe 进程PID: {pid}')
        return _session

    def get_current_version(self):
        """
        获取当前微信版本签名
        :return:
        """
        return self.current_version

    def load_script(self, js_name, on_message=None):
        """
        frida加载脚本
        :param js_name: javascript文件名
        :param on_message: 消息回调函数
        :return: frida script 对象
        """
        # 获取当前脚本文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 获取脚本文件路径
        js_path = os.path.join(current_dir, "js", self.current_version, js_name + ".js")

        # 判断文件是否存在
        if not os.path.isfile(js_path):
            return None

        # print("load script:", js_path)

        # 使用Frida创建JavaScript脚本
        script_code = open(js_path, 'r', encoding='utf-8').read()

        # 在Frida会话中加载JavaScript脚本
        script = self.session.create_script(script_code)

        # 设置回调函数
        if on_message:
            script.on('message', on_message)

        # 加载脚本
        script.load()

        return script
