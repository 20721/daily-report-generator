"""初始化向导窗口 - 3 页可切换"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional


class WizardWindow(tk.Toplevel):
    def __init__(self, parent, config_service, on_complete: Callable):
        super().__init__(parent)
        self.config_service = config_service
        self.on_complete = on_complete
        self.current_page = 0
        self.total_pages = 3
        
        self.title('🎉 欢迎使用每日报表生成器 - 初始化向导')
        self.geometry('700x550')
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # 人员模块临时存储
        self.personnel_modules = []
        
        self._create_ui()
        self._show_page(0)
    
    def _create_ui(self):
        """创建 UI"""
        # 标题
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(title_frame, text='🎉 欢迎使用每日报表生成器', 
                 font=('Microsoft YaHei UI', 14, 'bold')).pack()
        ttk.Label(title_frame, text='初始化向导', 
                 font=('Microsoft YaHei UI', 10)).pack(pady=5)
        
        # 进度标签
        self.progress_label = ttk.Label(self, text='第 1 页 / 共 3 页', 
                                       font=('Microsoft YaHei UI', 10))
        self.progress_label.pack(pady=5)
        
        # 页面容器
        self.page_frame = ttk.Frame(self, padding=20)
        self.page_frame.pack(fill='both', expand=True)
        
        # 按钮区
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill='x')
        
        self.prev_btn = ttk.Button(btn_frame, text='上一步', 
                                   command=self._prev_page, state='disabled')
        self.prev_btn.pack(side='left', padx=5)
        
        self.next_btn = ttk.Button(btn_frame, text='下一步', 
                                   command=self._next_page)
        self.next_btn.pack(side='right', padx=5)
    
    def _clear_page(self):
        """清除当前页内容"""
        for widget in self.page_frame.winfo_children():
            widget.destroy()
    
    def _show_page(self, page_num: int):
        """显示指定页"""
        self._clear_page()
        self.current_page = page_num
        
        # 更新进度
        self.progress_label.config(text=f'第 {page_num + 1} 页 / 共 {self.total_pages} 页')
        
        # 更新按钮
        self.prev_btn.config(state='normal' if page_num > 0 else 'disabled')
        self.next_btn.config(text='完成配置' if page_num == self.total_pages - 1 else '下一步')
        
        # 显示对应页面
        if page_num == 0:
            self._show_basic_info_page()
        elif page_num == 1:
            self._show_personnel_page()
        elif page_num == 2:
            self._show_comm_page()
    
    def _show_basic_info_page(self):
        """第 1 页：基础信息"""
        ttk.Label(self.page_frame, text='基础信息', 
                 font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w', pady=10)
        
        # 表单
        form_frame = ttk.Frame(self.page_frame)
        form_frame.pack(fill='x')
        
        # 单位名称
        ttk.Label(form_frame, text='单位名称:', width=12).grid(row=0, column=0, sticky='w', pady=5)
        self.unit_name_entry = ttk.Entry(form_frame, width=40)
        self.unit_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # 所在区域
        ttk.Label(form_frame, text='所在区域:', width=12).grid(row=1, column=0, sticky='w', pady=5)
        self.region_entry = ttk.Entry(form_frame, width=40)
        self.region_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # 井号
        ttk.Label(form_frame, text='井    号:', width=12).grid(row=2, column=0, sticky='w', pady=5)
        self.well_name_entry = ttk.Entry(form_frame, width=40)
        self.well_name_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # 设计井深
        ttk.Label(form_frame, text='设计井深:', width=12).grid(row=3, column=0, sticky='w', pady=5)
        self.design_depth_entry = ttk.Entry(form_frame, width=40)
        self.design_depth_entry.grid(row=3, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text='m').grid(row=3, column=2, sticky='w', padx=5)
    
    def _show_personnel_page(self):
        """第 2 页：人员配置"""
        ttk.Label(self.page_frame, text='人员配置', 
                 font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w', pady=10)
        
        # 人员列表
        list_frame = ttk.LabelFrame(self.page_frame, text='人员模块列表', padding=10)
        list_frame.pack(fill='both', expand=True, pady=5)
        
        # 创建滚动区域
        canvas = tk.Canvas(list_frame, height=200)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 默认人员模块
        default_modules = [
            ('919 队', 'chinese'),
            ('外聘厨师', 'chinese'),
            ('外聘大夫', 'chinese'),
            ('当地雇员', 'local'),
            ('士兵', 'local'),
            ('安保', 'local')
        ]
        
        self.personnel_entries = []
        for i, (label, category) in enumerate(default_modules):
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill='x', pady=2)
            
            ttk.Label(frame, text=label, width=15).pack(side='left', padx=5)
            
            # 人数下拉框（1-20）
            count_var = tk.StringVar(value='1')
            count_combo = ttk.Combobox(frame, textvariable=count_var, width=5, state='readonly')
            count_combo['values'] = [str(i) for i in range(1, 21)]
            count_combo.set('1')
            count_combo.pack(side='left', padx=5)
            
            ttk.Label(frame, text='人').pack(side='left', padx=2)
            ttk.Label(frame, text=f'({category})', width=10).pack(side='left', padx=5)
            
            self.personnel_entries.append({
                'label': label,
                'category': category,
                'count_var': count_var
            })
        
        # 添加按钮
        ttk.Button(self.page_frame, text='+ 添加人员模块', 
                  command=self._add_personnel_module).pack(pady=5)
    
    def _add_personnel_module(self):
        """添加人员模块"""
        # 简化实现：添加一个默认模块
        dialog = tk.Toplevel(self)
        dialog.title('添加人员模块')
        dialog.geometry('400x200')
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text='模块标签:').pack(pady=5)
        label_entry = ttk.Entry(dialog, width=40)
        label_entry.pack(pady=5)
        
        ttk.Label(dialog, text='类别:').pack(pady=5)
        category_var = tk.StringVar(value='chinese')
        ttk.Radiobutton(dialog, text='中方人员', variable=category_var, value='chinese').pack()
        ttk.Radiobutton(dialog, text='当地雇员', variable=category_var, value='local').pack()
        
        def on_add():
            label = label_entry.get().strip()
            if label:
                frame = ttk.Frame(self.page_frame.winfo_children()[0].winfo_children()[0])
                frame.pack(fill='x', pady=2)
                
                ttk.Label(frame, text=label, width=15).pack(side='left', padx=5)
                
                count_var = tk.StringVar(value='1')
                count_combo = ttk.Combobox(frame, textvariable=count_var, width=5, state='readonly')
                count_combo['values'] = [str(i) for i in range(1, 21)]
                count_combo.set('1')
                count_combo.pack(side='left', padx=5)
                
                ttk.Label(frame, text='人').pack(side='left', padx=2)
                ttk.Label(frame, text=f'({category_var.get()})', width=10).pack(side='left', padx=5)
                
                self.personnel_entries.append({
                    'label': label,
                    'category': category_var.get(),
                    'count_var': count_var
                })
                
                dialog.destroy()
        
        ttk.Button(dialog, text='确定', command=on_add).pack(pady=10)
    
    def _show_comm_page(self):
        """第 3 页：通讯信息"""
        ttk.Label(self.page_frame, text='通讯信息', 
                 font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w', pady=10)
        
        # 表单
        form_frame = ttk.Frame(self.page_frame)
        form_frame.pack(fill='both', expand=True)
        
        # 通讯情况
        ttk.Label(form_frame, text='通讯情况:').grid(row=0, column=0, sticky='w', pady=5)
        self.comm_status_entry = ttk.Entry(form_frame, width=50)
        self.comm_status_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # 平台经理电话
        ttk.Label(form_frame, text='平台经理电话:').grid(row=1, column=0, sticky='w', pady=5)
        self.manager_phone_entry = ttk.Entry(form_frame, width=50)
        self.manager_phone_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Thuraya 电话
        ttk.Label(form_frame, text='Thuraya 电话:').grid(row=2, column=0, sticky='w', pady=5)
        self.thuraya_phone_entry = ttk.Entry(form_frame, width=50)
        self.thuraya_phone_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # 卫星内线
        ttk.Label(form_frame, text='卫星内线:').grid(row=3, column=0, sticky='w', pady=5)
        self.sat_internal_entry = ttk.Entry(form_frame, width=50)
        self.sat_internal_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # 卫星外线
        ttk.Label(form_frame, text='卫星外线:').grid(row=4, column=0, sticky='w', pady=5)
        self.sat_external_entry = ttk.Entry(form_frame, width=50)
        self.sat_external_entry.grid(row=4, column=1, pady=5, padx=5)
        
        # 安全情况
        ttk.Label(form_frame, text='安全情况:').grid(row=5, column=0, sticky='w', pady=5)
        self.security_entry = ttk.Entry(form_frame, width=50)
        self.security_entry.grid(row=5, column=1, pady=5, padx=5)
    
    def _prev_page(self):
        """上一页"""
        if self.current_page > 0:
            self._show_page(self.current_page - 1)
    
    def _next_page(self):
        """下一页"""
        # 验证当前页
        if not self._validate_current_page():
            return
        
        if self.current_page < self.total_pages - 1:
            self._show_page(self.current_page + 1)
        else:
            self._finish()
    
    def _validate_current_page(self) -> bool:
        """验证当前页"""
        if self.current_page == 0:
            # 验证基础信息
            if not self.unit_name_entry.get().strip():
                messagebox.showerror('错误', '单位名称不能为空', parent=self)
                return False
            if not self.region_entry.get().strip():
                messagebox.showerror('错误', '所在区域不能为空', parent=self)
                return False
            if not self.well_name_entry.get().strip():
                messagebox.showerror('错误', '井号不能为空', parent=self)
                return False
            try:
                depth = int(self.design_depth_entry.get().strip())
                if depth <= 0:
                    raise ValueError()
            except:
                messagebox.showerror('错误', '设计井深必须是大于 0 的整数', parent=self)
                return False
        
        return True
    
    def _finish(self):
        """完成配置"""
        # 收集数据
        config = self.config_service._get_default_config()
        
        # 固定字段
        config['fixed_fields']['unit_name'] = self.unit_name_entry.get().strip()
        config['fixed_fields']['region'] = self.region_entry.get().strip()
        config['fixed_fields']['well_name'] = self.well_name_entry.get().strip()
        try:
            config['fixed_fields']['design_depth'] = int(self.design_depth_entry.get().strip())
        except:
            config['fixed_fields']['design_depth'] = 0
        
        # 人员模块
        for entry in self.personnel_entries:
            config['personnel_modules'].append({
                'id': entry['label'],
                'label': entry['label'],
                'count': int(entry['count_var'].get()),
                'category': entry['category'],
                'is_default': True
            })
        
        # 通讯信息
        config['comm_info']['status'] = self.comm_status_entry.get().strip()
        config['comm_info']['manager_phone'] = self.manager_phone_entry.get().strip()
        config['comm_info']['thuraya_phone'] = self.thuraya_phone_entry.get().strip()
        config['comm_info']['sat_internal'] = self.sat_internal_entry.get().strip()
        config['comm_info']['sat_external'] = self.sat_external_entry.get().strip()
        config['comm_info']['security'] = self.security_entry.get().strip()
        
        # 默认工况词条
        config['work_tokens']['all_tokens'] = [
            '下套管', '循环', '固井', '候凝', '安装套管头', '安装 BOP', '试压',
            'BOP 试压', '组合二开钻具', '下钻', '钻塞', '二开钻进'
        ]
        
        # 保存配置
        self.config_service.config = config
        success, message = self.config_service.save()
        
        if success:
            messagebox.showinfo('成功', '配置已保存！\n\n现在可以开始使用每日报表生成器了。', parent=self)
            self.on_complete()
            self.destroy()
        else:
            messagebox.showerror('错误', f'保存配置失败：{message}', parent=self)
