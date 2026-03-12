#!/usr/bin/env python3
"""每日报表生成器 - Tkinter 轻量版"""
import sys
import os

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

from report_app.ui.main_window_tk import MainWindow
from report_app.utils.logger import setup_logger

logger = setup_logger()

if __name__ == '__main__':
    logger.info("程序启动 - Tkinter 版本")
    app = MainWindow()
    app.mainloop()
