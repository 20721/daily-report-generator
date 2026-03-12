"""首次运行向导 - Tkinter 版本"""
import tkinter as tk
from tkinter import ttk, messagebox
from report_app.utils.logger import get_logger

logger = get_logger()


class WizardDialog(tk.Toplevel):
    def __init__(self, parent, config_service):
        super().__init__(parent)
        self.config_service = config_service
        self.config = config_service.config
        self.result = False
        
        self.title('🎉 欢迎使用每日报表生成器 - 首次配置向导')
        self.geometry('700x550')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        """创建 UI"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 进度标签
        self.progress_label = ttk.Label(main_frame, text='第 1 页 / 共 3 页', 
                                       font=('Microsoft YaHei UI', 11))
        self.progress_label.pack(pady=10)
        
        # 页面容器
        self.page_frame = ttk.Frame(main_frame)
        self.page_frame.pack(fill='both', expand=True, pady=10)
        
        self.current_page = 0
        self._show_page(0)
        
        # 按钮区
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)
        
        btn_frame.columnconfigure(0, weight=1)
        
        self.prev_btn = ttk.Button(btn_frame, text='上一步', command=self._prev_page,
                                   state='disabled')
        self.prev_btn.grid(row=0, column=0, sticky='w', padx=5)
        
        self.next_btn = ttk.Button(btn_frame, text='下一步', command=self._next_page)
        self.next_btn.grid(row=0, column=1, sticky='e', padx=5)
    
    def _show_page(self, page_num):
        """显示页面"""
        # 清除旧内容
        for widget in self.page_frame.winfo_children():
            widget.destroy()
        
        if page_num == 0:
            self._page_basic_info()
        elif page_num == 1:
            self._page_personnel()
        elif page_num == 2:
            self._page_contact()
        
        # 更新按钮状态
        self.prev_btn.config(state='normal' if page_num > 0 else 'disabled')
        self.next_btn.config(text='完成' if page_num == 2 else '下一步')
    
    def _page_basic_info(self):
        """第 1 页：基础信息"""
        ttk.Label(self.page_frame, text='📋 基础信息', 
                 font=('Microsoft YaHei UI', 14, 'bold')).pack(pady=10)
        
        form = ttk.Frame(self.page_frame)
        form.pack(fill='x', padx=20)
        
        fields = [
            ('单位名称:', self.config.basic_info.unit_name),
            ('所在区域:', self.config.basic_info.region),
            ('井号:', self.config.basic_info.well_name),
            ('设计井深 (m):', str(self.config.basic_info.design_depth_value)),
        ]
        
        self.basic_entries = []
        for label, default in fields:
            row = ttk.Frame(form)
            row.pack(fill='x', pady=5)
            
            ttk.Label(row, text=label, width=15).pack(side='left')
            entry = ttk.Entry(row, width=40)
            entry.pack(side='left', padx=5)
            entry.insert(0, default)
            self.basic_entries.append(entry)
    
    def _page_personnel(self):
        """第 2 页：人员配置"""
        ttk.Label(self.page_frame, text='👥 人员配置', 
                 font=('Microsoft YaHei UI', 14, 'bold')).pack(pady=10)
        
        form = ttk.Frame(self.page_frame)
        form.pack(fill='x', padx=20)
        
        # 查找默认人员配置
        unit_chinese = 14
        cook = 3
        local = 29
        soldier = 8
        manager_name = '赵铁寨'
        
        for item in self.config.personnel_items:
            if item.id == 'unit_chinese':
                unit_chinese = item.count
            elif item.id == 'cook':
                cook = item.count
            elif item.id == 'local':
                local = item.count
            elif item.id == 'soldier':
                soldier = item.count
            elif item.id == 'manager':
                manager_name = item.special_name
        
        ttk.Label(form, text='本单位中方人数:').pack(anchor='w', pady=5)
        self.unit_chinese_spin = ttk.Spinbox(form, from_=0, to=500, width=20)
        self.unit_chinese_spin.pack(anchor='w', pady=5)
        self.unit_chinese_spin.set(unit_chinese)
        
        ttk.Label(form, text='外聘厨师人数:').pack(anchor='w', pady=5)
        self.cook_spin = ttk.Spinbox(form, from_=0, to=50, width=20)
        self.cook_spin.pack(anchor='w', pady=5)
        self.cook_spin.set(cook)
        
        ttk.Label(form, text='本单位当地雇员人数:').pack(anchor='w', pady=5)
        self.local_spin = ttk.Spinbox(form, from_=0, to=500, width=20)
        self.local_spin.pack(anchor='w', pady=5)
        self.local_spin.set(local)
        
        ttk.Label(form, text='士兵人数:').pack(anchor='w', pady=5)
        self.soldier_spin = ttk.Spinbox(form, from_=0, to=100, width=20)
        self.soldier_spin.pack(anchor='w', pady=5)
        self.soldier_spin.set(soldier)
        
        ttk.Label(form, text='基地经理姓名:').pack(anchor='w', pady=5)
        self.manager_name_entry = ttk.Entry(form, width=40)
        self.manager_name_entry.pack(anchor='w', pady=5)
        self.manager_name_entry.insert(0, manager_name)
    
    def _page_contact(self):
        """第 3 页：通讯信息"""
        ttk.Label(self.page_frame, text='📞 通讯信息', 
                 font=('Microsoft YaHei UI', 14, 'bold')).pack(pady=10)
        
        form = ttk.Frame(self.page_frame)
        form.pack(fill='x', padx=20)
        
        contact = self.config.contact_info
        
        ttk.Label(form, text='平台经理电话:').pack(anchor='w', pady=5)
        self.manager_phone_entry = ttk.Entry(form, width=40)
        self.manager_phone_entry.pack(anchor='w', pady=5)
        self.manager_phone_entry.insert(0, contact.manager_phone)
        
        ttk.Label(form, text='Thuraya 电话:').pack(anchor='w', pady=5)
        self.thuraya_phone_entry = ttk.Entry(form, width=40)
        self.thuraya_phone_entry.pack(anchor='w', pady=5)
        self.thuraya_phone_entry.insert(0, contact.thuraya_phone)
        
        ttk.Label(form, text='通讯情况:').pack(anchor='w', pady=5)
        self.comm_status_entry = ttk.Entry(form, width=40)
        self.comm_status_entry.pack(anchor='w', pady=5)
        self.comm_status_entry.insert(0, contact.communication_status)
        
        ttk.Label(form, text='安全情况:').pack(anchor='w', pady=5)
        self.security_status_entry = ttk.Entry(form, width=40)
        self.security_status_entry.pack(anchor='w', pady=5)
        self.security_status_entry.insert(0, contact.security_status)
    
    def _next_page(self):
        """下一页"""
        if self.current_page < 2:
            self.current_page += 1
            self._show_page(self.current_page)
            self.progress_label.config(text=f'第 {self.current_page + 1} 页 / 共 3 页')
        else:
            self._finish()
    
    def _prev_page(self):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self._show_page(self.current_page)
            self.progress_label.config(text=f'第 {self.current_page + 1} 页 / 共 3 页')
    
    def _finish(self):
        """完成向导"""
        # 保存基础信息
        self.config.basic_info.unit_name = self.basic_entries[0].get()
        self.config.basic_info.region = self.basic_entries[1].get()
        self.config.basic_info.well_name = self.basic_entries[2].get()
        self.config.basic_info.design_depth_value = int(self.basic_entries[3].get() or 1000)
        
        # 保存人员配置
        for item in self.config.personnel_items:
            if item.id == 'unit_chinese':
                item.count = int(self.unit_chinese_spin.get())
            elif item.id == 'cook':
                item.count = int(self.cook_spin.get())
            elif item.id == 'local':
                item.count = int(self.local_spin.get())
            elif item.id == 'soldier':
                item.count = int(self.soldier_spin.get())
            elif item.id == 'manager':
                item.special_name = self.manager_name_entry.get()
        
        # 保存通讯信息
        self.config.contact_info.manager_phone = self.manager_phone_entry.get()
        self.config.contact_info.thuraya_phone = self.thuraya_phone_entry.get()
        self.config.contact_info.communication_status = self.comm_status_entry.get()
        self.config.contact_info.security_status = self.security_status_entry.get()
        
        # 保存配置
        if self.config_service.save(self.config):
            messagebox.showinfo('完成', '配置已保存！\n\n现在可以开始使用每日报表生成器了。')
            logger.info("向导完成，配置已保存")
            self.result = True
            self.destroy()
        else:
            messagebox.showerror('错误', '保存配置失败！')
