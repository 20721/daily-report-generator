"""主窗口 - 精简布局 + 实时预览"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pyperclip
import sys
import os
from pathlib import Path

# 获取程序目录
if getattr(sys, 'frozen', False):
    APP_DIR = Path(os.path.dirname(sys.executable))
else:
    APP_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

sys.path.insert(0, str(APP_DIR))

from report_app.services.config_service import ConfigService


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('🛢 每日报表生成器')
        self.geometry('1280x800')
        
        self.config_service = ConfigService()
        self.last_focus = 'today'  # today or next
        
        self._load_config()
        self._create_ui()
    
    def _load_config(self):
        """加载配置"""
        success, message = self.config_service.load()
        if not success:
            messagebox.showwarning('警告', message)
    
    def _create_ui(self):
        """创建 UI"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # 第一行：基础信息 | 人员信息 | 通讯信息
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=0, column=0, sticky='ew', pady=5)
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(2, weight=1)
        
        self._create_basic_info(info_frame, 0)
        self._create_personnel_info(info_frame, 1)
        self._create_comm_info(info_frame, 2)
        
        # 第二行：工况编辑
        work_frame = ttk.LabelFrame(main_frame, text='📝 工况编辑', padding=10)
        work_frame.grid(row=1, column=0, sticky='ew', pady=5)
        self._create_work_edit(work_frame)
        
        # 第三行：按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, sticky='ew', pady=10)
        self._create_buttons(btn_frame)
        
        # 第四行：版权信息
        copyright_frame = ttk.Frame(main_frame)
        copyright_frame.grid(row=3, column=0, sticky='ew', pady=5)
        ttk.Label(copyright_frame, text='By Freely QQ:20721  |  Pzxsky@Gmail.com',
                 font=('Microsoft YaHei UI', 9)).pack()
    
    def _create_basic_info(self, parent, col):
        """创建基础信息区"""
        frame = ttk.LabelFrame(parent, text='📋 基础信息', padding=10)
        frame.grid(row=0, column=col, sticky='nsew', padx=5)
        
        config = self.config_service.config
        fixed = config.get('fixed_fields', {})
        
        ttk.Label(frame, text=f"单位名称：{fixed.get('unit_name', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"所在区域：{fixed.get('region', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"井    号：{fixed.get('well_name', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"设计井深：{fixed.get('design_depth', 0)} m").pack(anchor='w', pady=2)
        
        ttk.Label(frame, text='当前井深:').pack(anchor='w', pady=(10, 2))
        self.current_depth_entry = ttk.Entry(frame, width=10)
        self.current_depth_entry.pack(anchor='w', pady=2)
        self.current_depth_entry.insert(0, '0')
    
    def _create_personnel_info(self, parent, col):
        """创建人员信息区"""
        frame = ttk.LabelFrame(parent, text='👥 人员信息', padding=10)
        frame.grid(row=0, column=col, sticky='nsew', padx=5)
        
        chinese_total = self.config_service.get_chinese_total()
        local_total = self.config_service.get_local_total()
        
        ttk.Label(frame, text=f'中方人员：{chinese_total}人', 
                 font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor='w', pady=2)
        
        for module in self.config_service.config.get('personnel_modules', []):
            if module.get('category') == 'chinese':
                ttk.Label(frame, text=f"  ├─ {module['label']} {module['count']}人").pack(anchor='w', pady=1)
        
        ttk.Label(frame, text=f'当地雇员：{local_total}人', 
                 font=('Microsoft YaHei UI', 10, 'bold')).pack(anchor='w', pady=(5, 2))
        
        for module in self.config_service.config.get('personnel_modules', []):
            if module.get('category') == 'local':
                ttk.Label(frame, text=f"  ├─ {module['label']} {module['count']}人").pack(anchor='w', pady=1)
    
    def _create_comm_info(self, parent, col):
        """创建通讯信息区"""
        frame = ttk.LabelFrame(parent, text='📞 通讯信息', padding=10)
        frame.grid(row=0, column=col, sticky='nsew', padx=5)
        
        comm = self.config_service.config.get('comm_info', {})
        
        ttk.Label(frame, text=f"通讯情况：{comm.get('status', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"平台经理：{comm.get('manager_phone', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"Thuraya: {comm.get('thuraya_phone', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"卫星内线：{comm.get('sat_internal', '')}").pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"安全情况：{comm.get('security', '')}").pack(anchor='w', pady=2)
    
    def _create_work_edit(self, parent):
        """创建工况编辑区"""
        # 今日工况和下步工况并排
        work_frame = ttk.Frame(parent)
        work_frame.pack(fill='x', pady=5)
        
        # 今日工况
        today_frame = ttk.LabelFrame(work_frame, text='今日工况', padding=5)
        today_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.today_work_text = tk.Text(today_frame, height=3, width=40)
        self.today_work_text.pack(fill='both', expand=True, pady=2)
        self.today_work_text.bind('<FocusIn>', lambda e: setattr(self, 'last_focus', 'today'))
        
        # 下步工况
        next_frame = ttk.LabelFrame(work_frame, text='下步工况', padding=5)
        next_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.next_work_text = tk.Text(next_frame, height=3, width=40)
        self.next_work_text.pack(fill='both', expand=True, pady=2)
        self.next_work_text.bind('<FocusIn>', lambda e: setattr(self, 'last_focus', 'next'))
        
        # 工况词条
        tokens_frame = ttk.LabelFrame(parent, text='🏷 工况词条（点击添加到当前焦点）', padding=5)
        tokens_frame.pack(fill='x', pady=5)
        
        tokens = self.config_service.config.get('work_tokens', {}).get('all_tokens', [])
        for token in tokens:
            btn = ttk.Button(tokens_frame, text=token, 
                           command=lambda t=token: self._add_token(t))
            btn.pack(side='left', padx=2, pady=2)
    
    def _add_token(self, text):
        """添加词条到当前焦点"""
        if self.last_focus == 'today':
            current = self.today_work_text.get('1.0', 'end-1c').strip()
            if current and not current.endswith(','):
                current += ','
            self.today_work_text.delete('1.0', 'end')
            self.today_work_text.insert('1.0', current + text)
        else:
            current = self.next_work_text.get('1.0', 'end-1c').strip()
            if current and not current.endswith(','):
                current += ','
            self.next_work_text.delete('1.0', 'end')
            self.next_work_text.insert('1.0', current + text)
    
    def _create_buttons(self, parent):
        """创建按钮区"""
        ttk.Button(parent, text='📋 生成报表', command=self._generate_report).pack(side='left', padx=5)
        ttk.Button(parent, text='👁 预览', command=self._preview_report).pack(side='left', padx=5)
        ttk.Button(parent, text='⚙️ 设置', command=self._show_settings).pack(side='left', padx=5)
    
    def _generate_report(self):
        """生成报表"""
        config = self.config_service.config
        fixed = config.get('fixed_fields', {})
        comm = config.get('comm_info', {})
        
        chinese_total = self.config_service.get_chinese_total()
        local_total = self.config_service.get_local_total()
        
        # 生成人员情况文本
        personnel_parts = []
        for m in config.get('personnel_modules', []):
            if m.get('category') == 'chinese':
                personnel_parts.append(f"{m['label']}{m['count']}人")
        
        chinese_detail = '，'.join(personnel_parts)
        
        local_parts = []
        for m in config.get('personnel_modules', []):
            if m.get('category') == 'local':
                local_parts.append(f"{m['label']}{m['count']}人")
        
        local_detail = '，'.join(local_parts)
        
        today_work = self.today_work_text.get('1.0', 'end-1c').strip()
        next_work = self.next_work_text.get('1.0', 'end-1c').strip()
        current_depth = self.current_depth_entry.get().strip() or '0'
        
        report = f"""1.单位名称：{fixed.get('unit_name', '')}
2.日期：{datetime.now().strftime('%Y.%m.%d')}
3.所在区域：{fixed.get('region', '')}
4.人员情况：中方人员{chinese_total}人（其中{chinese_detail}）{fixed.get('well_name', '')}当地雇员{local_total}人；{local_detail}。
5.生活物资储备天数：{fixed.get('supply_days', 30)}天；井场柴油{fixed.get('diesel_volume', 50)}方，可用{fixed.get('diesel_days', 15)}天。
6.井号：{fixed.get('well_name', '')} 设计井深：{fixed.get('design_depth', 0)} m
7.今日工况：{today_work}。
8.当前井深：{current_depth}m
9.下步工况：{next_work}。
10.通讯情况：{comm.get('status', '')}，平台经理：{comm.get('manager_phone', '')} Thuraya 电话：{comm.get('thuraya_phone', '')}卫星网络座机：{comm.get('sat_internal', '')} {comm.get('sat_external', '')} 安全情况：{comm.get('security', '')}"""
        
        # 复制到剪贴板
        pyperclip.copy(report)
        
        # 显示预览
        self._show_preview(report)
        
        messagebox.showinfo('成功', '报表已生成并复制到剪贴板！', parent=self)
    
    def _preview_report(self):
        """预览报表"""
        self._generate_report()
    
    def _show_preview(self, report_text):
        """显示预览窗口"""
        preview = tk.Toplevel(self)
        preview.title('📄 报表预览')
        preview.geometry('600x500')
        preview.transient(self)
        
        text = tk.Text(preview, wrap='word', font=('Consolas', 10))
        text.pack(fill='both', expand=True, padx=10, pady=10)
        text.insert('1.0', report_text)
        text.config(state='disabled')
        
        btn_frame = ttk.Frame(preview)
        btn_frame.pack(fill='x', pady=5)
        
        def on_copy():
            pyperclip.copy(report_text)
            messagebox.showinfo('成功', '已复制到剪贴板', parent=preview)
        
        ttk.Button(btn_frame, text='📋 复制', command=on_copy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='关闭', command=preview.destroy).pack(side='right', padx=5)
    
    def _show_settings(self):
        """显示设置（简化版）"""
        messagebox.showinfo('设置', '设置功能开发中...', parent=self)
