"""主窗口 - v6.1.2 弹窗位置修复版"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pyperclip
import sys
import os
from pathlib import Path
import json

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
        self.geometry('950x680')
        self.minsize(900, 650)
        
        self.config_service = ConfigService()
        self.last_focus = 'today'
        self.personnel_labels = {}
        
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
    
    def _auto_save(self, event=None):
        """自动保存当前数据"""
        config = self.config_service.config
        config['current_data'] = {
            'current_depth': self.current_depth_entry.get().strip(),
            'today_work': self.today_work_text.get('1.0', 'end-1c').strip(),
            'next_work': self.next_work_text.get('1.0', 'end-1c').strip()
        }
        self.config_service.save()
    
    def _center_dialog(self, dialog, width, height):
        """居中显示对话框"""
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_ui(self):
        """创建 UI"""
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)
        
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
        
        # 第三行：按钮（居中）
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)
        self._create_buttons(btn_frame)
        
        # 第四行：版权信息（右下角）
        copyright_frame = ttk.Frame(main_frame)
        copyright_frame.pack(fill='x', pady=5)
        ttk.Label(copyright_frame, text='By Freely QQ:20721 | Pzxsky@Gmail.com',
                 font=('Microsoft YaHei UI', 9)).pack(side='right')
    
    def _create_basic_info(self, parent, col):
        """创建基础信息区"""
        frame = ttk.LabelFrame(parent, text='📋 基础信息', padding=10)
        frame.pack(side='left', fill='both', expand=True, padx=5)
        
        config = self.config_service.config
        fixed = config.get('fixed_fields', {})
        
        ttk.Label(frame, text=f"单位：{fixed.get('unit_name', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"区域：{fixed.get('region', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"井号：{fixed.get('well_name', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"设计：{fixed.get('design_depth', 0)}m").pack(anchor='w', pady=1)
        
        depth_frame = ttk.Frame(frame)
        depth_frame.pack(anchor='w', pady=(5, 2))
        ttk.Label(depth_frame, text='当前井深:').pack(side='left')
        self.current_depth_entry = ttk.Entry(depth_frame, width=8)
        self.current_depth_entry.pack(side='left', padx=5)
        ttk.Label(depth_frame, text='m').pack(side='left')
        self.current_depth_entry.bind('<KeyRelease>', self._auto_save)
        
        current_data = config.get('current_data', {})
        self.current_depth_entry.insert(0, current_data.get('current_depth', '0'))
    
    def _create_personnel_info(self, parent, col):
        """创建人员信息区"""
        frame = ttk.LabelFrame(parent, text='👥 人员信息', padding=10)
        frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # 标题行
        title_frame = ttk.Frame(frame)
        title_frame.pack(fill='x')
        
        self.chinese_total_label = ttk.Label(title_frame, text='中方人员：0 人', font=('Microsoft YaHei UI', 9, 'bold'))
        self.chinese_total_label.pack(side='left', padx=5)
        
        self.local_total_label = ttk.Label(title_frame, text='当地雇员：0 人', font=('Microsoft YaHei UI', 9, 'bold'))
        self.local_total_label.pack(side='right', padx=5)
        
        # 可滚动区域
        scroll_frame = ttk.Frame(frame)
        scroll_frame.pack(fill='both', expand=True, pady=5)
        
        canvas = tk.Canvas(scroll_frame, height=100)
        scrollbar = ttk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
        self.personnel_scrollable = ttk.Frame(canvas)
        
        self.personnel_scrollable.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.personnel_scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        canvas.bind('<MouseWheel>', on_mousewheel)
        canvas.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, 'units'))
        canvas.bind('<Button-5>', lambda e: canvas.yview_scroll(1, 'units'))
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self._refresh_personnel_display()
        
        # 分隔线
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=5)
        
        # 其他人员（原领导模块）
        other_frame = ttk.LabelFrame(frame, text='其他人员', padding=5)
        other_frame.pack(fill='both', expand=True)
        
        ttk.Button(other_frame, text='+ 添加', command=self._add_other_person).pack(anchor='w', pady=2)
        
        self._refresh_other_persons_display(other_frame)
    
    def _refresh_personnel_display(self):
        """刷新人员信息显示"""
        for widget in self.personnel_scrollable.winfo_children():
            widget.destroy()
        
        config = self.config_service.config
        chinese_modules = [m for m in config.get('personnel_modules', []) if m.get('category') == 'chinese' and not m.get('is_other')]
        local_modules = [m for m in config.get('personnel_modules', []) if m.get('category') == 'local' and not m.get('is_other')]
        
        chinese_total = sum(m.get('count', 0) for m in chinese_modules)
        local_total = sum(m.get('count', 0) for m in local_modules)
        
        self.chinese_total_label.config(text=f'中方人员：{chinese_total}人')
        self.local_total_label.config(text=f'当地雇员：{local_total}人')
        
        # 中方人员
        chinese_frame = ttk.LabelFrame(self.personnel_scrollable, text='中方', padding=3)
        chinese_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        for module in chinese_modules:
            self._create_person_item(chinese_frame, module, 'chinese')
        
        ttk.Button(chinese_frame, text='+ 添加', command=lambda: self._add_person_module('chinese')).pack(pady=2)
        
        # 当地雇员
        local_frame = ttk.LabelFrame(self.personnel_scrollable, text='当地', padding=3)
        local_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        for module in local_modules:
            self._create_person_item(local_frame, module, 'local')
        
        ttk.Button(local_frame, text='+ 添加', command=lambda: self._add_person_module('local')).pack(pady=2)
    
    def _refresh_other_persons_display(self, parent):
        """刷新其他人员显示"""
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button):
                continue
            widget.destroy()
        
        config = self.config_service.config
        other_modules = [m for m in config.get('personnel_modules', []) if m.get('is_other')]
        
        if other_modules:
            for module in other_modules:
                item_frame = ttk.Frame(parent)
                item_frame.pack(fill='x', pady=1)
                ttk.Label(item_frame, text=f"├─ {module['label']} ({module['category']})", wraplength=200).pack(side='left')
                ttk.Button(item_frame, text='×', width=2, command=lambda m=module: self._delete_other_person(m)).pack(side='right')
        else:
            ttk.Label(parent, text='（无）').pack(anchor='w', pady=5)
    
    def _create_person_item(self, parent, module, category):
        """创建人员项"""
        item_frame = ttk.Frame(parent)
        item_frame.pack(fill='x', pady=1)
        ttk.Label(item_frame, text=f"{module['label']}:", width=12).pack(side='left')
        
        count_var = tk.StringVar(value=str(module['count']))
        count_combo = ttk.Combobox(item_frame, textvariable=count_var, width=4, state='normal')
        count_combo['values'] = [str(i) for i in range(1, 21)]
        count_combo.pack(side='left', padx=2)
        
        def on_change(*args):
            self._update_person_count(module, count_var.get(), category)
        count_var.trace_add('write', on_change)
        count_combo.bind('<KeyRelease>', lambda e: self._update_person_count(module, count_var.get(), category))
        
        ttk.Label(item_frame, text='人').pack(side='left')
    
    def _update_person_count(self, module, new_count, category):
        """更新人员数量"""
        try:
            module['count'] = int(new_count)
            self._refresh_personnel_display()
            self._auto_save()
        except:
            pass
    
    def _add_person_module(self, category):
        """添加人员模块"""
        dialog = tk.Toplevel(self)
        dialog.title('添加人员模块')
        self._center_dialog(dialog, 300, 150)
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text='模块标签:').pack(pady=5)
        label_entry = ttk.Entry(dialog, width=30)
        label_entry.pack(pady=5)
        
        def on_add():
            label = label_entry.get().strip()
            if label:
                self.config_service.config['personnel_modules'].append({
                    'id': label,
                    'label': label,
                    'count': 1,
                    'category': category,
                    'is_other': False
                })
                self._auto_save()
                dialog.destroy()
                self._refresh_personnel_display()
        
        ttk.Button(dialog, text='确定', command=on_add).pack(pady=10)
    
    def _add_other_person(self):
        """添加其他人员（简化版）"""
        dialog = tk.Toplevel(self)
        dialog.title('添加其他人员')
        self._center_dialog(dialog, 350, 140)
        dialog.transient(self)
        dialog.grab_set()
        
        # 第一行：输入框
        ttk.Label(dialog, text='人员标签:').pack(pady=2)
        label_entry = ttk.Entry(dialog, width=40)
        label_entry.pack(pady=2)
        
        # 第二行：类别选择 + 保存按钮
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=5)
        
        category_var = tk.StringVar(value='chinese')
        ttk.Radiobutton(btn_frame, text='中方', variable=category_var, value='chinese').pack(side='left', padx=10)
        ttk.Radiobutton(btn_frame, text='外籍', variable=category_var, value='local').pack(side='left', padx=10)
        
        def on_save():
            label = label_entry.get().strip()
            if label:
                self.config_service.config['personnel_modules'].append({
                    'id': label,
                    'label': label,
                    'count': 1,
                    'category': category_var.get(),
                    'is_other': True
                })
                self._auto_save()
                dialog.destroy()
                self._refresh_personnel_display()
        
        ttk.Button(btn_frame, text='保存', command=on_save).pack(side='left', padx=10)
    
    def _delete_other_person(self, module):
        """删除其他人员"""
        result = messagebox.askyesno('确认', f'确定删除"{module.get("label", "")}"吗？')
        
        if result:
            self.config_service.config['personnel_modules'] = [
                m for m in self.config_service.config['personnel_modules']
                if m.get('id') != module.get('id')
            ]
            self._auto_save()
            self._refresh_personnel_display()
    
    def _create_comm_info(self, parent, col):
        """创建通讯信息区"""
        frame = ttk.LabelFrame(parent, text='📞 通讯信息', padding=10)
        frame.pack(side='left', fill='both', expand=True, padx=5)
        
        comm = self.config_service.config.get('comm_info', {})
        
        ttk.Label(frame, text=f"通讯：{comm.get('status', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"经理：{comm.get('manager_phone', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"Thuraya: {comm.get('thuraya_phone', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"卫星内线：{comm.get('sat_internal', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"卫星外线：{comm.get('sat_external', '')}").pack(anchor='w', pady=1)
        ttk.Label(frame, text=f"安全：{comm.get('security', '')}").pack(anchor='w', pady=1)
    
    def _create_work_edit(self, parent):
        """创建工况编辑区（自动换行）"""
        work_frame = ttk.Frame(parent)
        work_frame.pack(fill='x', pady=5)
        
        # 今日工况
        today_frame = ttk.LabelFrame(work_frame, text='今日工况', padding=5)
        today_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.today_work_text = tk.Text(today_frame, height=2, width=25)
        self.today_work_text.pack(fill='both', expand=True, pady=2)
        self.today_work_text.bind('<FocusIn>', lambda e: setattr(self, 'last_focus', 'today'))
        self.today_work_text.bind('<KeyRelease>', self._auto_save)
        
        # 下步工况
        next_frame = ttk.LabelFrame(work_frame, text='下步工况', padding=5)
        next_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.next_work_text = tk.Text(next_frame, height=2, width=25)
        self.next_work_text.pack(fill='both', expand=True, pady=2)
        self.next_work_text.bind('<FocusIn>', lambda e: setattr(self, 'last_focus', 'next'))
        self.next_work_text.bind('<KeyRelease>', self._auto_save)
        
        current_data = self.config_service.config.get('current_data', {})
        self.today_work_text.insert('1.0', current_data.get('today_work', ''))
        self.next_work_text.insert('1.0', current_data.get('next_work', ''))
        
        # 工况词条（自动换行）
        tokens_frame = ttk.LabelFrame(parent, text='🏷 工况词条', padding=5)
        tokens_frame.pack(fill='x', pady=5)
        
        # 添加工况按钮（靠右）
        add_btn = ttk.Button(tokens_frame, text='+ 添加工况', command=self._add_token_dialog)
        add_btn.pack(side='right', padx=5)
        
        # 可滚动区域
        canvas = tk.Canvas(tokens_frame, height=60)
        canvas.pack(fill='both', expand=True, pady=2)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        canvas.bind('<MouseWheel>', on_mousewheel)
        canvas.bind('<Button-4>', lambda e: canvas.yview_scroll(-1, 'units'))
        canvas.bind('<Button-5>', lambda e: canvas.yview_scroll(1, 'units'))
        
        scrollable = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        
        # 使用 Frame 实现自动换行
        token_container = ttk.Frame(scrollable)
        token_container.pack(fill='both', expand=True)
        
        tokens = self.config_service.config.get('work_tokens', {}).get('all_tokens', [])
        if not tokens:
            tokens = ['下套管', '循环', '固井', '候凝', '安装套管头', '安装 BOP', '试压']
        
        for token in tokens:
            btn = ttk.Button(token_container, text=token, command=lambda t=token: self._add_token(t))
            btn.pack(side='left', padx=2, pady=2)
            btn.bind('<Button-3>', lambda e, t=token: self._show_token_menu(e, t))
    
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
        self._auto_save()
    
    def _add_token_dialog(self):
        """添加工况对话框"""
        dialog = tk.Toplevel(self)
        dialog.title('添加工况')
        self._center_dialog(dialog, 300, 120)
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text='工况名称:').pack(pady=5)
        token_entry = ttk.Entry(dialog, width=30)
        token_entry.pack(pady=5)
        
        def on_add():
            token = token_entry.get().strip()
            if token:
                self.config_service.config['work_tokens']['all_tokens'].append(token)
                self._auto_save()
                dialog.destroy()
                self._refresh_ui()
        
        ttk.Button(dialog, text='确定', command=on_add).pack(pady=10)
    
    def _show_token_menu(self, event, token):
        """显示词条右键菜单"""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='修改', command=lambda: self._edit_token(token))
        menu.add_command(label='删除', command=lambda: self._delete_token(token))
        menu.post(event.x_root, event.y_root)
    
    def _edit_token(self, token):
        """修改词条"""
        dialog = tk.Toplevel(self)
        dialog.title('修改词条')
        self._center_dialog(dialog, 300, 120)
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text='新名称:').pack(pady=5)
        token_entry = ttk.Entry(dialog, width=30)
        token_entry.insert(0, token)
        token_entry.pack(pady=5)
        
        def on_save():
            new_token = token_entry.get().strip()
            if new_token:
                tokens = self.config_service.config['work_tokens']['all_tokens']
                if token in tokens:
                    idx = tokens.index(token)
                    tokens[idx] = new_token
                self._auto_save()
                dialog.destroy()
                self._refresh_ui()
        
        ttk.Button(dialog, text='保存', command=on_save).pack(pady=10)
    
    def _delete_token(self, token):
        """删除词条"""
        result = messagebox.askyesno('确认', f'确定删除词条"{token}"吗？')
        
        if result:
            self.config_service.config['personnel_modules'] = [
                self._auto_save()
                self._refresh_ui()
    
    def _create_buttons(self, parent):
        """创建按钮区"""
        btn_container = ttk.Frame(parent)
        btn_container.pack()
        
        ttk.Button(btn_container, text='📋 生成报表', command=self._generate_report).pack(side='left', padx=10)
        ttk.Button(btn_container, text='⚙️ 设置', command=self._show_settings).pack(side='left', padx=10)
    
    def _generate_report_text(self):
        """生成报表文本"""
        config = self.config_service.config
        fixed = config.get('fixed_fields', {})
        comm = config.get('comm_info', {})
        
        chinese_modules = [m for m in config.get('personnel_modules', []) if m.get('category') == 'chinese' and not m.get('is_other')]
        local_modules = [m for m in config.get('personnel_modules', []) if m.get('category') == 'local' and not m.get('is_other')]
        other_modules = [m for m in config.get('personnel_modules', []) if m.get('is_other')]
        
        chinese_total = sum(m.get('count', 0) for m in chinese_modules)
        local_total = sum(m.get('count', 0) for m in local_modules)
        
        chinese_detail = '，'.join([f"{m['label']}{m['count']}人" for m in chinese_modules])
        local_detail = '；'.join([f"{m['label']}{m['count']}人" for m in local_modules])
        
        other_notes = [m['label'] for m in other_modules]
        
        today_work = self.today_work_text.get('1.0', 'end-1c').strip()
        next_work = self.next_work_text.get('1.0', 'end-1c').strip()
        current_depth = self.current_depth_entry.get().strip() or '0'
        
        report = f"""1.单位名称：{fixed.get('unit_name', '')}
2.日期：{datetime.now().strftime('%Y.%m.%d')}
3.所在区域：{fixed.get('region', '')}
4.人员情况：中方人员{chinese_total}人（其中{chinese_detail}）{fixed.get('well_name', '')}当地雇员{local_total}人；{local_detail}。{"，".join(other_notes)}。
5.生活物资储备天数：{fixed.get('supply_days', 30)}天；井场柴油{fixed.get('diesel_volume', 50)}方，可用{fixed.get('diesel_days', 15)}天。
6.井号：{fixed.get('well_name', '')} 设计井深：{fixed.get('design_depth', 0)} m
7.今日工况：{today_work}。
8.当前井深：{current_depth}m
9.下步工况：{next_work}。
10.通讯情况：{comm.get('status', '')}，平台经理：{comm.get('manager_phone', '')} Thuraya 电话：{comm.get('thuraya_phone', '')}卫星网络座机：{comm.get('sat_internal', '')} {comm.get('sat_external', '')} 安全情况：{comm.get('security', '')}"""
        
        return report
    
    def _generate_report(self):
        """生成报表：保存 + 复制 + 预览窗口"""
        report = self._generate_report_text()
        self._save_report(report)
        pyperclip.copy(report)
        self._show_preview_window(report)
    
    def _show_preview_window(self, report_text):
        """显示预览窗口（居中）"""
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
            messagebox.showinfo('成功', '已复制到剪贴板', parent=preview)
        
        ttk.Button(btn_frame, text='📋 复制', command=on_copy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='关闭', command=preview.destroy).pack(side='right', padx=5)
    
    def _save_report(self, content):
        """保存报表到文件"""
        if getattr(sys, 'frozen', False):
            base_dir = Path(os.path.dirname(sys.executable))
        else:
            base_dir = APP_DIR
        
        reports_dir = base_dir / 'reports' / datetime.now().strftime('%Y-%m')
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = reports_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _show_settings(self):
        """显示设置（居中）"""
        settings = tk.Toplevel(self)
        settings.title('⚙️ 设置')
        self._center_dialog(settings, 500, 450)
        settings.transient(self)
        
        ttk.Label(settings, text='配置管理', font=('Microsoft YaHei UI', 12, 'bold')).pack(pady=10)
        
        config_text = tk.Text(settings, wrap='word', height=20)
        config_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        config_str = json.dumps(self.config_service.config, ensure_ascii=False, indent=2)
        config_text.insert('1.0', config_str)
        
        btn_frame = ttk.Frame(settings)
        btn_frame.pack(fill='x', pady=10)
        
        def on_save():
            try:
                new_config = json.loads(config_text.get('1.0', 'end'))
                self.config_service.config = new_config
                self.config_service.save()
                messagebox.showinfo('成功', '配置已保存！', parent=settings)
                self._refresh_ui()
            except Exception as e:
                messagebox.showerror('错误', f'配置格式错误：{e}', parent=settings)
        
        def on_reload():
            self.config_service.load()
            self._refresh_ui()
            settings.destroy()
        
        def on_wizard():
            result = messagebox.askyesno('确认', '重新运行向导将覆盖当前配置，确定吗？', parent=settings):
                settings.destroy()
                self._run_wizard()
        
        ttk.Button(btn_frame, text='💾 保存重载', command=on_save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='🔄 重新运行向导', command=on_wizard).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='关闭', command=settings.destroy).pack(side='right', padx=5)
    
    def _refresh_ui(self):
        """刷新 UI"""
        for widget in self.winfo_children():
            widget.destroy()
        self._load_config()
        self._create_ui()
    
    def _run_wizard(self):
        """重新运行向导"""
        from report_app.ui.wizard_window_tk import WizardWindow
        
        root = tk.Tk()
        root.withdraw()
        
        def on_complete():
            root.destroy()
            self.destroy()
            app = MainWindow()
            app.mainloop()
        
        wizard = WizardWindow(root, self.config_service, on_complete)
        root.mainloop()
