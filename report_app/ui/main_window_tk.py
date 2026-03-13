"""主窗口 - 修复布局居中问题"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pyperclip
import sys
import os
from pathlib import Path
import json

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
        self.geometry('1100x750')  # 优化默认大小
        self.minsize(1000, 700)  # 最小大小
        
        self.config_service = ConfigService()
        self.last_focus = 'today'
        
        self._load_config()
        self._create_ui()
    
    def _load_config(self):
        """加载配置"""
        success, message = self.config_service.load()
        if not success:
            messagebox.showwarning('警告', message)
        
        if not self.config_service.config.get('work_tokens', {}).get('all_tokens'):
            self.config_service.config['work_tokens'] = {
                'all_tokens': [
                    '下套管', '循环', '固井', '候凝', '安装套管头', '安装 BOP', '试压',
                    'BOP 试压', '组合二开钻具', '下钻', '钻塞', '二开钻进'
                ],
                'today': [],
                'next': []
            }
    
    def _create_ui(self):
        """创建 UI"""
        # 主容器 - 使用 Frame 包裹，内容不会拉伸
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)
        
        # 内容区域 - 固定宽度，居中显示
        main_frame = ttk.Frame(container, padding=10)
        main_frame.pack(fill='x', padx=20, pady=10)
        
        # 第一行：基础信息 | 人员信息 | 通讯信息
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=5)
        
        self._create_basic_info(info_frame, 0)
        self._create_personnel_info(info_frame, 1)
        self._create_comm_info(info_frame, 2)
        
        # 第二行：工况编辑
        work_frame = ttk.LabelFrame(main_frame, text='📝 工况编辑', padding=10)
        work_frame.pack(fill='x', pady=5)
        self._create_work_edit(work_frame)
        
        # 第三行：按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)
        self._create_buttons(btn_frame)
        
        # 第四行：版权信息
        copyright_frame = ttk.Frame(main_frame)
        copyright_frame.pack(fill='x', pady=5)
        ttk.Label(copyright_frame, text='By Freely QQ:20721  |  Pzxsky@Gmail.com',
                 font=('Microsoft YaHei UI', 9)).pack()
    
    def _create_basic_info(self, parent, col):
        """创建基础信息区"""
        frame = ttk.LabelFrame(parent, text='📋 基础信息', padding=10)
        frame.pack(side='left', fill='both', expand=True, padx=5)
        
        config = self.config_service.config
        fixed = config.get('fixed_fields', {})
        
        ttk.Label(frame, text=f"单位名称：{fixed.get('unit_name', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"所在区域：{fixed.get('region', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"井    号：{fixed.get('well_name', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"设计井深：{fixed.get('design_depth', 0)} m", wraplength=150).pack(anchor='w', pady=2)
        
        ttk.Label(frame, text='当前井深:').pack(anchor='w', pady=(10, 2))
        self.current_depth_entry = ttk.Entry(frame, width=10)
        self.current_depth_entry.pack(anchor='w', pady=2)
        self.current_depth_entry.insert(0, '0')
    
    def _create_personnel_info(self, parent, col):
        """创建人员信息区"""
        frame = ttk.LabelFrame(parent, text='👥 人员信息', padding=10)
        frame.pack(side='left', fill='both', expand=True, padx=5)
        
        chinese_modules = [m for m in self.config_service.config.get('personnel_modules', []) if m.get('category') == 'chinese']
        local_modules = [m for m in self.config_service.config.get('personnel_modules', []) if m.get('category') == 'local']
        leader_modules = [m for m in self.config_service.config.get('personnel_modules', []) if m.get('is_leader')]
        
        chinese_total = sum(m.get('count', 0) for m in chinese_modules)
        local_total = sum(m.get('count', 0) for m in local_modules)
        
        # 上半部分：中方人员 + 当地雇员 横排
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill='both', expand=True)
        
        # 中方人员（左侧）
        chinese_frame = ttk.LabelFrame(top_frame, text=f'中方人员：{chinese_total}人', padding=5)
        chinese_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        for module in chinese_modules:
            ttk.Label(chinese_frame, text=f"├─ {module['label']} {module['count']}人", 
                     wraplength=120).pack(anchor='w', pady=1)
        
        # 当地雇员（右侧）
        local_frame = ttk.LabelFrame(top_frame, text=f'当地雇员：{local_total}人', padding=5)
        local_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        for module in local_modules:
            ttk.Label(local_frame, text=f"├─ {module['label']} {module['count']}人", 
                     wraplength=120).pack(anchor='w', pady=1)
        
        # 分隔线
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=5)
        
        # 下半部分：领导模块
        leader_frame = ttk.LabelFrame(frame, text='领导模块', padding=5)
        leader_frame.pack(fill='both', expand=True)
        
        if leader_modules:
            for module in leader_modules:
                leader_text = f"{module.get('title', '')}{module.get('name', '')}"
                if module.get('action'):
                    leader_text += f" ({module['action']})"
                ttk.Label(leader_frame, text=f"├─ {leader_text}", 
                         wraplength=200).pack(anchor='w', pady=1)
        else:
            ttk.Label(leader_frame, text='（无）').pack(anchor='w', pady=5)
    
    def _create_comm_info(self, parent, col):
        """创建通讯信息区"""
        frame = ttk.LabelFrame(parent, text='📞 通讯信息', padding=10)
        frame.pack(side='left', fill='both', expand=True, padx=5)
        
        comm = self.config_service.config.get('comm_info', {})
        
        ttk.Label(frame, text=f"通讯：{comm.get('status', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"经理：{comm.get('manager_phone', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"Thuraya: {comm.get('thuraya_phone', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"卫星：{comm.get('sat_internal', '')}", wraplength=150).pack(anchor='w', pady=2)
        ttk.Label(frame, text=f"安全：{comm.get('security', '')}", wraplength=150).pack(anchor='w', pady=2)
    
    def _create_work_edit(self, parent):
        """创建工况编辑区"""
        work_frame = ttk.Frame(parent)
        work_frame.pack(fill='x', pady=5)
        
        # 今日工况
        today_frame = ttk.LabelFrame(work_frame, text='今日工况', padding=5)
        today_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.today_work_text = tk.Text(today_frame, height=2, width=30)
        self.today_work_text.pack(fill='both', expand=True, pady=2)
        self.today_work_text.bind('<FocusIn>', lambda e: setattr(self, 'last_focus', 'today'))
        
        # 下步工况
        next_frame = ttk.LabelFrame(work_frame, text='下步工况', padding=5)
        next_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.next_work_text = tk.Text(next_frame, height=2, width=30)
        self.next_work_text.pack(fill='both', expand=True, pady=2)
        self.next_work_text.bind('<FocusIn>', lambda e: setattr(self, 'last_focus', 'next'))
        
        # 工况词条
        tokens_frame = ttk.LabelFrame(parent, text='🏷 工况词条（点击添加到当前焦点）', padding=5)
        tokens_frame.pack(fill='x', pady=5)
        
        tokens = self.config_service.config.get('work_tokens', {}).get('all_tokens', [])
        if not tokens:
            tokens = [
                '下套管', '循环', '固井', '候凝', '安装套管头', '安装 BOP', '试压',
                'BOP 试压', '组合二开钻具', '下钻', '钻塞', '二开钻进'
            ]
        
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
        ttk.Button(parent, text='👁 预览', command=self._preview_only).pack(side='left', padx=5)
        ttk.Button(parent, text='⚙️ 设置', command=self._show_settings).pack(side='left', padx=5)
    
    def _generate_report_text(self):
        """生成报表文本"""
        config = self.config_service.config
        fixed = config.get('fixed_fields', {})
        comm = config.get('comm_info', {})
        
        chinese_modules = [m for m in config.get('personnel_modules', []) if m.get('category') == 'chinese']
        local_modules = [m for m in config.get('personnel_modules', []) if m.get('category') == 'local']
        leader_modules = [m for m in config.get('personnel_modules', []) if m.get('is_leader')]
        
        chinese_total = sum(m.get('count', 0) for m in chinese_modules)
        local_total = sum(m.get('count', 0) for m in local_modules)
        
        chinese_detail = '，'.join([f"{m['label']}{m['count']}人" for m in chinese_modules])
        local_detail = '；'.join([f"{m['label']}{m['count']}人" for m in local_modules])
        
        leader_notes = []
        for leader in leader_modules:
            if leader.get('action'):
                leader_notes.append(f"{leader.get('title', '')}{leader.get('name', '')}{leader['action']}")
        
        today_work = self.today_work_text.get('1.0', 'end-1c').strip()
        next_work = self.next_work_text.get('1.0', 'end-1c').strip()
        current_depth = self.current_depth_entry.get().strip() or '0'
        
        report = f"""1.单位名称：{fixed.get('unit_name', '')}
2.日期：{datetime.now().strftime('%Y.%m.%d')}
3.所在区域：{fixed.get('region', '')}
4.人员情况：中方人员{chinese_total}人（其中{chinese_detail}）{fixed.get('well_name', '')}当地雇员{local_total}人；{local_detail}。{"，".join(leader_notes)}。
5.生活物资储备天数：{fixed.get('supply_days', 30)}天；井场柴油{fixed.get('diesel_volume', 50)}方，可用{fixed.get('diesel_days', 15)}天。
6.井号：{fixed.get('well_name', '')} 设计井深：{fixed.get('design_depth', 0)} m
7.今日工况：{today_work}。
8.当前井深：{current_depth}m
9.下步工况：{next_work}。
10.通讯情况：{comm.get('status', '')}，平台经理：{comm.get('manager_phone', '')} Thuraya 电话：{comm.get('thuraya_phone', '')}卫星网络座机：{comm.get('sat_internal', '')} {comm.get('sat_external', '')} 安全情况：{comm.get('security', '')}"""
        
        return report
    
    def _generate_report(self):
        """生成报表：保存 + 复制 + 预览"""
        report = self._generate_report_text()
        self._save_report(report)
        pyperclip.copy(report)
        self._show_preview_center(report)
    
    def _preview_only(self):
        """仅预览：不保存不复制"""
        report = self._generate_report_text()
        self._show_preview_center(report)
    
    def _save_report(self, content):
        """保存报表到文件"""
        if getattr(sys, 'frozen', False):
            base_dir = Path(os.path.dirname(sys.executable))
        else:
            base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
        
        reports_dir = base_dir / 'reports' / datetime.now().strftime('%Y-%m')
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = reports_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _show_preview_center(self, report_text):
        """显示预览窗口（居中显示）"""
        preview = tk.Toplevel(self)
        preview.title('📄 报表预览')
        
        width = 650
        height = 550
        x = (preview.winfo_screenwidth() // 2) - (width // 2)
        y = (preview.winfo_screenheight() // 2) - (height // 2)
        preview.geometry(f'{width}x{height}+{x}+{y}')
        
        preview.transient(self)
        
        text = tk.Text(preview, wrap='word', font=('Consolas', 10))
        text.pack(fill='both', expand=True, padx=15, pady=15)
        text.insert('1.0', report_text)
        text.config(state='disabled')
        
        btn_frame = ttk.Frame(preview)
        btn_frame.pack(fill='x', pady=10)
        
        def on_copy():
            pyperclip.copy(report_text)
        
        ttk.Button(btn_frame, text='📋 复制', command=on_copy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='关闭', command=preview.destroy).pack(side='right', padx=5)
    
    def _show_settings(self):
        """显示设置"""
        settings = tk.Toplevel(self)
        settings.title('⚙️ 设置')
        settings.geometry('500x400')
        settings.transient(self)
        
        ttk.Label(settings, text='配置信息（只读）', 
                 font=('Microsoft YaHei UI', 12, 'bold')).pack(pady=10)
        
        config_text = tk.Text(settings, wrap='word', height=15)
        config_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        config_str = json.dumps(self.config_service.config, ensure_ascii=False, indent=2)
        config_text.insert('1.0', config_str)
        config_text.config(state='disabled')
        
        btn_frame = ttk.Frame(settings)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text='关闭', command=settings.destroy).pack(side='right', padx=5)
        
        ttk.Button(btn_frame, text='重新运行向导', 
                  command=lambda: self._run_wizard(settings)).pack(side='left', padx=5)
    
    def _run_wizard(self, parent):
        """重新运行向导"""
        from report_app.ui.wizard_window_tk import WizardWindow
        
        if messagebox.askyesno('确认', '重新运行向导将覆盖当前配置，确定吗？', parent=parent):
            parent.destroy()
            root = tk.Tk()
            root.withdraw()
            
            def on_complete():
                root.destroy()
                self.destroy()
                app = MainWindow()
                app.mainloop()
            
            wizard = WizardWindow(root, self.config_service, on_complete)
            root.mainloop()
