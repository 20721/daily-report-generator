"""主窗口 - Tkinter 版本 (轻量级)"""
import sys
import os
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip

# 获取程序目录
if getattr(sys, 'frozen', False):
    APP_DIR = Path(os.path.dirname(sys.executable))
else:
    APP_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

sys.path.insert(0, str(APP_DIR))

from report_app.services.config_service import ConfigService
from report_app.services.report_service import ReportService
from report_app.ui.wizard.wizard_window_tk import WizardDialog
from report_app.utils.logger import get_logger

logger = get_logger()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('🛢 每日报表生成器')
        self.geometry('1280x820')
        
        self.config_service = ConfigService()
        self.config = self.config_service.load()
        self.report_service = ReportService(self.config)
        
        self.last_focused_operation = 'today'
        
        self._create_ui()
        self._load_config_to_ui()
        
        if not self.config_service.has_config():
            self.after(500, self._show_wizard)
    
    def _create_ui(self):
        """创建 UI"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # 基础信息区
        self._create_basic_section(main_frame)
        
        # 工况编辑区
        self._create_operation_section(main_frame)
        
        # 人员通讯区
        self._create_staff_section(main_frame)
        
        # 按钮区
        self._create_buttons(main_frame)
    
    def _create_basic_section(self, parent):
        """基础信息区"""
        basic_frame = ttk.LabelFrame(parent, text='📋 基础信息', padding=10)
        basic_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        # 第一行
        row0 = ttk.Frame(basic_frame)
        row0.pack(fill='x', pady=3)
        
        ttk.Label(row0, text='单位名称:', width=10).pack(side='left', padx=5)
        self.unit_name_entry = ttk.Entry(row0, width=20)
        self.unit_name_entry.pack(side='left', padx=5)
        
        ttk.Label(row0, text='日期:', width=5).pack(side='left', padx=10)
        self.date_entry = ttk.Entry(row0, width=15)
        self.date_entry.pack(side='left', padx=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y.%m.%d'))
        
        ttk.Label(row0, text='区域:', width=5).pack(side='left', padx=10)
        self.region_entry = ttk.Entry(row0, width=10)
        self.region_entry.pack(side='left', padx=5)
        
        # 第二行
        row1 = ttk.Frame(basic_frame)
        row1.pack(fill='x', pady=3)
        
        ttk.Label(row1, text='井号:', width=10).pack(side='left', padx=5)
        self.well_name_entry = ttk.Entry(row1, width=25)
        self.well_name_entry.pack(side='left', padx=5)
        
        ttk.Label(row1, text='设计井深:', width=10).pack(side='left', padx=10)
        self.design_depth_entry = ttk.Entry(row1, width=15)
        self.design_depth_entry.pack(side='left', padx=5)
        
        ttk.Label(row1, text='当前井深:', width=10).pack(side='left', padx=10)
        self.current_depth_entry = ttk.Entry(row1, width=10)
        self.current_depth_entry.pack(side='left', padx=5)
    
    def _create_operation_section(self, parent):
        """工况编辑区"""
        op_frame = ttk.LabelFrame(parent, text='📝 工况编辑', padding=10)
        op_frame.grid(row=1, column=0, sticky='nsew', pady=5, padx=(0, 5))
        
        # 今日工况
        ttk.Label(op_frame, text='今日工况:').pack(anchor='w', pady=3)
        self.today_work_text = tk.Text(op_frame, height=4, width=50)
        self.today_work_text.pack(fill='x', pady=3)
        self.today_work_text.bind('<FocusIn>', lambda e: self._set_focus('today'))
        
        # 下步工况
        ttk.Label(op_frame, text='下步工况:').pack(anchor='w', pady=3)
        self.next_work_text = tk.Text(op_frame, height=4, width=50)
        self.next_work_text.pack(fill='x', pady=3)
        self.next_work_text.bind('<FocusIn>', lambda e: self._set_focus('next'))
        
        # 工况词条
        ttk.Label(op_frame, text='🏷 工况词条（点击添加到当前焦点）:').pack(anchor='w', pady=5)
        tokens_frame = ttk.Frame(op_frame)
        tokens_frame.pack(fill='x')
        
        self._create_token_buttons(tokens_frame)
    
    def _create_token_buttons(self, parent):
        """创建词条按钮"""
        default_tokens = ['下套管', '循环', '固井', '候凝', '安装套管头', 
                         '安装 BOP', '试压', 'BOP 试压', '组合二开钻具', 
                         '下钻', '钻塞', '二开钻进']
        
        for token in default_tokens:
            btn = ttk.Button(parent, text=token, 
                           command=lambda t=token: self._add_token(t))
            btn.pack(side='left', padx=3, pady=3)
    
    def _create_staff_section(self, parent):
        """人员通讯区"""
        staff_frame = ttk.LabelFrame(parent, text='👥 人员与通讯', padding=10)
        staff_frame.grid(row=1, column=1, sticky='nsew', pady=5, padx=(5, 0))
        
        # 人员信息标签
        self.personnel_label = ttk.Label(staff_frame, text='', font=('Microsoft YaHei UI', 10))
        self.personnel_label.pack(anchor='w', pady=5)
        
        # 通讯信息
        ttk.Label(staff_frame, text='通讯情况:').pack(anchor='w', pady=3)
        self.comm_status_entry = ttk.Entry(staff_frame, width=40)
        self.comm_status_entry.pack(anchor='w', pady=3)
        
        ttk.Label(staff_frame, text='平台经理电话:').pack(anchor='w', pady=3)
        self.manager_phone_entry = ttk.Entry(staff_frame, width=40)
        self.manager_phone_entry.pack(anchor='w', pady=3)
        
        ttk.Label(staff_frame, text='Thuraya 电话:').pack(anchor='w', pady=3)
        self.thuraya_phone_entry = ttk.Entry(staff_frame, width=40)
        self.thuraya_phone_entry.pack(anchor='w', pady=3)
        
        ttk.Label(staff_frame, text='安全情况:').pack(anchor='w', pady=3)
        self.security_status_entry = ttk.Entry(staff_frame, width=40)
        self.security_status_entry.pack(anchor='w', pady=3)
    
    def _create_buttons(self, parent):
        """按钮区"""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text='📋 生成报表', command=self._generate_report).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='📋 复制到剪贴板', command=self._copy_to_clipboard).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='👁 预览', command=self._preview_report).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='⚙️ 设置', command=self._show_wizard).pack(side='left', padx=5)
    
    def _set_focus(self, focus):
        """设置焦点"""
        self.last_focused_operation = focus
    
    def _add_token(self, token_text):
        """添加词条"""
        if self.last_focused_operation == 'today':
            current = self.today_work_text.get('1.0', 'end-1c').strip()
            if current:
                if not current.endswith(','):
                    current += ','
                current += token_text
            else:
                current = token_text
            self.today_work_text.delete('1.0', 'end')
            self.today_work_text.insert('1.0', current)
        else:
            current = self.next_work_text.get('1.0', 'end-1c').strip()
            if current:
                if not current.endswith(','):
                    current += ','
                current += token_text
            else:
                current = token_text
            self.next_work_text.delete('1.0', 'end')
            self.next_work_text.insert('1.0', current)
    
    def _load_config_to_ui(self):
        """加载配置"""
        basic = self.config.basic_info
        self.unit_name_entry.insert(0, basic.unit_name)
        self.region_entry.insert(0, basic.region)
        self.well_name_entry.insert(0, basic.well_name)
        self.design_depth_entry.insert(0, f"{basic.design_depth_value} {basic.design_depth_unit}")
        
        contact = self.config.contact_info
        self.comm_status_entry.insert(0, contact.communication_status)
        self.manager_phone_entry.insert(0, contact.manager_phone)
        self.thuraya_phone_entry.insert(0, contact.thuraya_phone)
        self.security_status_entry.insert(0, contact.security_status)
        
        # 更新人员标签
        snapshot = self.report_service.calculate_personnel_snapshot()
        self.personnel_label.config(
            text=f"中方{snapshot.chinese_total}人 | 当地雇员{snapshot.local_foreign_total}人"
        )
    
    def _show_wizard(self):
        """显示向导"""
        dialog = WizardDialog(self, self.config_service)
        if dialog.result:
            self.config = self.config_service.config
            self.report_service.config = self.config
            self._load_config_to_ui()
    
    def _collect_data(self):
        """收集数据"""
        design_depth = self.design_depth_entry.get().split()
        depth_value = int(design_depth[0]) if design_depth else 0
        depth_unit = design_depth[1] if len(design_depth) > 1 else 'm'
        
        from report_app.models.report_models import DailyReportData, PersonnelSnapshot
        
        return DailyReportData(
            unit_name=self.unit_name_entry.get(),
            report_date=self.date_entry.get(),
            region=self.region_entry.get(),
            personnel_snapshot=self.report_service.calculate_personnel_snapshot(),
            supply_days=self.config.basic_info.supply_days_default,
            diesel_volume=self.config.basic_info.diesel_volume_default,
            diesel_days=self.config.basic_info.diesel_days_default,
            well_name=self.well_name_entry.get(),
            design_depth_value=depth_value,
            design_depth_unit=depth_unit,
            today_operations_text=self.today_work_text.get('1.0', 'end-1c').strip(),
            current_depth=int(self.current_depth_entry.get() or 0),
            next_operations_text=self.next_work_text.get('1.0', 'end-1c').strip(),
            communication_status=self.comm_status_entry.get(),
            manager_phone=self.manager_phone_entry.get(),
            thuraya_phone=self.thuraya_phone_entry.get(),
            sat_phone_internal=self.config.contact_info.sat_phone_internal,
            sat_phone_external=self.config.contact_info.sat_phone_external,
            security_status=self.security_status_entry.get()
        )
    
    def _generate_report(self):
        """生成报表"""
        try:
            data = self._collect_data()
            report_text = self.report_service.generate_report(data)
            
            # 显示预览窗口
            preview = tk.Toplevel(self)
            preview.title('📄 报表预览')
            preview.geometry('600x400')
            
            text_widget = tk.Text(preview, wrap='word', font=('Consolas', 10))
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget.insert('1.0', report_text)
            text_widget.config(state='disabled')
            
            logger.info("报表已生成")
        except Exception as e:
            logger.error(f"生成报表失败：{e}")
            messagebox.showerror('错误', f'生成报表失败：{e}')
    
    def _copy_to_clipboard(self):
        """复制到剪贴板"""
        try:
            data = self._collect_data()
            report_text = self.report_service.generate_report(data)
            pyperclip.copy(report_text)
            messagebox.showinfo('成功', '报表已复制到剪贴板！')
        except Exception as e:
            messagebox.showerror('错误', f'复制失败：{e}')
    
    def _preview_report(self):
        """预览"""
        self._generate_report()


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
