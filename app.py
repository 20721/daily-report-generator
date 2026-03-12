#!/usr/bin/env python3
"""每日报表生成器 v6.0.2 - 入口文件（修复启动逻辑）"""
import sys
import os
from pathlib import Path
from tkinter import Tk

# 获取程序目录
if getattr(sys, 'frozen', False):
    APP_DIR = Path(os.path.dirname(sys.executable))
else:
    APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, str(APP_DIR))

from report_app.services.config_service import ConfigService
from report_app.ui.wizard_window_tk import WizardWindow
from report_app.ui.main_window_tk import MainWindow


def main():
    """主函数 - 简化启动逻辑"""
    # 创建根窗口
    root = Tk()
    root.withdraw()  # 先隐藏根窗口
    
    # 加载配置
    config_service = ConfigService()
    success, message = config_service.load()
    
    if not success or not config_service.has_config():
        # 没有配置，显示向导
        print(f'提示：{message}')
        print('启动初始化向导...')
        
        # 显示向导并等待完成
        wizard = WizardWindow(root, config_service, lambda: None)
        wizard.wait_window()  # 等待向导窗口关闭
        
        # 向导完成后，销毁根窗口并创建主窗口
        root.destroy()
        app = MainWindow()
        app.mainloop()
    else:
        # 有配置，直接显示主窗口
        print(f'提示：{message}')
        print('启动主程序...')
        root.destroy()
        app = MainWindow()
        app.mainloop()


if __name__ == '__main__':
    main()
