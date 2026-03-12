#!/usr/bin/env python3
"""每日报表生成器 v6.0.0 - 入口文件"""
import sys
import os
from pathlib import Path

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
    """主函数"""
    config_service = ConfigService()
    
    # 尝试加载配置
    success, message = config_service.load()
    
    if not success or not config_service.has_config():
        # 没有配置，显示向导
        print(f'提示：{message}')
        print('启动初始化向导...')
        
        # 创建隐藏根窗口
        root = Tk()
        root.withdraw()
        
        def on_wizard_complete():
            root.destroy()
            # 重新启动主程序
            main()
        
        wizard = WizardWindow(root, config_service, on_wizard_complete)
        root.mainloop()
    else:
        # 有配置，显示主窗口
        print(f'提示：{message}')
        print('启动主程序...')
        app = MainWindow()
        app.mainloop()


if __name__ == '__main__':
    # 需要从 tkinter 导入 Tk
    from tkinter import Tk
    main()
