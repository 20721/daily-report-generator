#!/usr/bin/env python3
"""每日报表生成器 v6.0.6 - 修复窗口显示问题"""
import sys
import os
import logging
from pathlib import Path
from tkinter import Tk

# 设置日志
log_file = 'DailyReport.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
    """主函数 - 修复窗口显示"""
    logger.info('='*60)
    logger.info('程序启动')
    logger.info(f'Python 版本：{sys.version}')
    logger.info(f'程序目录：{APP_DIR}')
    logger.info(f'工作目录：{os.getcwd()}')
    logger.info(f'冻结状态：{getattr(sys, "frozen", False)}')
    
    try:
        # 创建根窗口（不隐藏！）
        logger.info('创建根窗口...')
        root = Tk()
        logger.info(f'根窗口创建成功：{root}')
        logger.info(f'根窗口句柄：{root.winfo_id() if root.winfo_exists() else "N/A"}')
        
        # 不隐藏根窗口，而是设置透明或最小化
        # root.withdraw()  # ← 不要隐藏！
        root.attributes('-alpha', 0)  # 设置为完全透明
        logger.info('根窗口已设置为透明')
        
        # 加载配置
        logger.info('加载配置...')
        config_service = ConfigService()
        success, message = config_service.load()
        logger.info(f'配置加载结果：success={success}, message={message}')
        logger.info(f'是否有配置：{config_service.has_config()}')
        
        if not success or not config_service.has_config():
            # 没有配置，显示向导
            logger.warning('没有配置，启动初始化向导...')
            
            # 显示向导并等待完成
            wizard = WizardWindow(root, config_service, lambda: None)
            logger.info(f'向导窗口创建：{wizard}')
            logger.info(f'向导窗口句柄：{wizard.winfo_id() if wizard.winfo_exists() else "N/A"}')
            logger.info('等待向导窗口关闭...')
            wizard.wait_window()
            logger.info('向导窗口已关闭')
            
            # 向导完成后，销毁根窗口并创建主窗口
            logger.info('销毁根窗口...')
            root.destroy()
            logger.info('根窗口已销毁')
            
            logger.info('创建主窗口...')
            app = MainWindow()
            logger.info(f'主窗口创建成功：{app}')
            logger.info('启动主循环...')
            app.mainloop()
            logger.info('主循环结束')
        else:
            # 有配置，直接显示主窗口
            logger.info('配置已存在，启动主程序...')
            logger.info('销毁根窗口...')
            root.destroy()
            logger.info('根窗口已销毁')
            
            logger.info('创建主窗口...')
            app = MainWindow()
            logger.info(f'主窗口创建成功：{app}')
            logger.info('启动主循环...')
            app.mainloop()
            logger.info('主循环结束')
            
    except Exception as e:
        logger.error(f'程序异常：{type(e).__name__}: {e}', exc_info=True)
        raise
    finally:
        logger.info('='*60)
        logger.info('程序退出')


if __name__ == '__main__':
    main()
