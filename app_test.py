#!/usr/bin/env python3
"""每日报表生成器 - 极简测试版本"""
import sys
import os
import logging
from pathlib import Path

# 设置日志
log_file = 'DailyReport_debug.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info('='*60)
logger.info('极简测试版本启动')
logger.info(f'Python: {sys.version}')
logger.info(f'Frozen: {getattr(sys, "frozen", False)}')

try:
    from tkinter import Tk, ttk, messagebox
    logger.info('Tkinter 导入成功')
    
    # 测试 1: 创建根窗口
    logger.info('测试 1: 创建根窗口...')
    root = Tk()
    logger.info(f'根窗口创建：{root}')
    logger.info(f'根窗口 ID: {root.winfo_id()}')
    
    # 测试 2: 设置窗口属性
    logger.info('测试 2: 设置窗口属性...')
    root.title('🛢 测试窗口')
    root.geometry('400x300')
    logger.info(f'窗口大小：{root.winfo_geometry()}')
    
    # 测试 3: 添加标签
    logger.info('测试 3: 添加标签...')
    label = ttk.Label(root, text='如果你看到这个窗口，说明 Tkinter 正常工作！', 
                     font=('Microsoft YaHei UI', 12))
    label.pack(pady=50)
    logger.info('标签添加成功')
    
    # 测试 4: 添加按钮
    logger.info('测试 4: 添加按钮...')
    def on_click():
        logger.info('按钮被点击')
        messagebox.showinfo('成功', 'Tkinter 工作正常！')
    
    btn = ttk.Button(root, text='点击测试', command=on_click)
    btn.pack(pady=10)
    logger.info('按钮添加成功')
    
    # 测试 5: 显示窗口
    logger.info('测试 5: 显示窗口...')
    root.attributes('-topmost', True)  # 置顶显示
    root.update()
    logger.info('窗口已更新')
    
    # 测试 6: 启动主循环
    logger.info('测试 6: 启动主循环...')
    logger.info('窗口应该已经显示了！')
    root.mainloop()
    logger.info('主循环结束')
    
except Exception as e:
    logger.error(f'异常：{type(e).__name__}: {e}', exc_info=True)
    import traceback
    logger.error(traceback.format_exc())
    
    # 创建错误文件
    with open('error.txt', 'w', encoding='utf-8') as f:
        f.write(f'错误类型：{type(e).__name__}\n')
        f.write(f'错误信息：{e}\n')
        f.write(f'\n堆栈跟踪:\n{traceback.format_exc()}\n')
    logger.error('错误已保存到 error.txt')

logger.info('='*60)
