"""主窗口 - PySide6"""
import sys
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QLineEdit, QDateEdit, QPushButton, 
                                QTextEdit, QGroupBox, QScrollArea, QFrame,
                                QMessageBox, QMenuBar, QMenu, QAction, QSplitter)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from report_app.services.config_service import ConfigService
from report_app.services.report_service import ReportService
from report_app.models.report_models import DailyReportData, PersonnelSnapshot
from report_app.ui.wizard.wizard_window import WizardDialog
from report_app.utils.logger import get_logger

logger = get_logger()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_service = ConfigService()
        self.config = self.config_service.load()
        self.report_service = ReportService(self.config)
        
        self.last_focused_operation = 'today'  # today or next
        
        self._init_ui()
        self._load_config_to_ui()
        
        # 检查首次运行
        if not self.config_service.has_config():
            self._show_wizard()
    
    def _init_ui(self):
        """初始化 UI"""
        self.setWindowTitle('🛢 每日报表生成器')
        self.setMinimumSize(1280, 820)
        
        # 创建菜单栏
        self._create_menu()
        
        # 主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 顶部基础信息区
        self._create_basic_info_section(layout)
        
        # 中部编辑区（左右分栏）
        self._create_edit_section(layout)
        
        # 底部按钮区
        self._create_buttons(layout)
    
    def _create_menu(self):
        """创建菜单"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        file_menu.addAction('新建当日报表', self._new_report)
        file_menu.addAction('导出 TXT', self._export_txt)
        file_menu.addSeparator()
        file_menu.addAction('退出', self.close)
        
        # 配置菜单
        config_menu = menubar.addMenu('配置')
        config_menu.addAction('重新运行初始化向导', self._show_wizard)
        config_menu.addAction('管理人员模块', self._manage_personnel)
        config_menu.addAction('管理工况词条', self._manage_tokens)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具')
        tools_menu.addAction('复制报表到剪贴板', self._copy_to_clipboard)
        tools_menu.addAction('预览报表', self._preview_report)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        help_menu.addAction('使用说明', self._show_help)
        help_menu.addAction('关于', self._show_about)
    
    def _create_basic_info_section(self, layout):
        """创建基础信息区"""
        group = QGroupBox('📋 基础信息')
        layout.addWidget(group)
        
        form_layout = QVBoxLayout()
        group.setLayout(form_layout)
        
        # 第一行
        row1 = QHBoxLayout()
        row1.addWidget(QLabel('单位名称:'))
        self.unit_name_edit = QLineEdit()
        row1.addWidget(self.unit_name_edit)
        
        row1.addWidget(QLabel('日期:'))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        row1.addWidget(self.date_edit)
        
        row1.addWidget(QLabel('区域:'))
        self.region_edit = QLineEdit()
        row1.addWidget(self.region_edit)
        
        form_layout.addLayout(row1)
        
        # 第二行
        row2 = QHBoxLayout()
        row2.addWidget(QLabel('井号:'))
        self.well_name_edit = QLineEdit()
        row2.addWidget(self.well_name_edit)
        
        row2.addWidget(QLabel('设计井深:'))
        self.design_depth_edit = QLineEdit()
        row2.addWidget(self.design_depth_edit)
        
        row2.addWidget(QLabel('当前井深:'))
        self.current_depth_edit = QLineEdit()
        row2.addWidget(self.current_depth_edit)
        
        form_layout.addLayout(row2)
    
    def _create_edit_section(self, layout):
        """创建编辑区"""
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左侧：工况编辑区
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 今日工况
        left_layout.addWidget(QLabel('📝 今日工况:'))
        self.today_work_edit = QTextEdit()
        self.today_work_edit.setMaximumHeight(100)
        self.today_work_edit.focusInEvent = lambda e: self._set_focus('today')
        left_layout.addWidget(self.today_work_edit)
        
        # 下步工况
        left_layout.addWidget(QLabel('📝 下步工况:'))
        self.next_work_edit = QTextEdit()
        self.next_work_edit.setMaximumHeight(100)
        self.next_work_edit.focusInEvent = lambda e: self._set_focus('next')
        left_layout.addWidget(self.next_work_edit)
        
        # 工况词条
        left_layout.addWidget(QLabel('🏷 工况词条（点击添加到当前焦点）:'))
        self.tokens_layout = QHBoxLayout()
        left_layout.addLayout(self.tokens_layout)
        
        splitter.addWidget(left_widget)
        
        # 右侧：人员与通讯区
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 人员情况（简化版）
        right_layout.addWidget(QLabel('👥 人员情况（在配置中管理）:'))
        self.personnel_info_label = QLabel()
        right_layout.addWidget(self.personnel_info_label)
        
        # 通讯信息
        right_layout.addWidget(QLabel('📞 通讯信息:'))
        self.comm_status_edit = QLineEdit()
        right_layout.addWidget(self.comm_status_edit)
        
        right_layout.addWidget(QLabel('平台经理电话:'))
        self.manager_phone_edit = QLineEdit()
        right_layout.addWidget(self.manager_phone_edit)
        
        right_layout.addWidget(QLabel('Thuraya 电话:'))
        self.thuraya_phone_edit = QLineEdit()
        right_layout.addWidget(self.thuraya_phone_edit)
        
        right_layout.addWidget(QLabel('安全情况:'))
        self.security_status_edit = QLineEdit()
        right_layout.addWidget(self.security_status_edit)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
    
    def _create_buttons(self, layout):
        """创建按钮区"""
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)
        
        self.generate_btn = QPushButton('📋 生成报表')
        self.generate_btn.clicked.connect(self._generate_report)
        btn_layout.addWidget(self.generate_btn)
        
        self.copy_btn = QPushButton('复制到剪贴板')
        self.copy_btn.clicked.connect(self._copy_to_clipboard)
        btn_layout.addWidget(self.copy_btn)
        
        self.preview_btn = QPushButton('👁 预览')
        self.preview_btn.clicked.connect(self._preview_report)
        btn_layout.addWidget(self.preview_btn)
        
        btn_layout.addStretch()
    
    def _set_focus(self, focus):
        """设置焦点"""
        self.last_focused_operation = focus
        logger.info(f"焦点切换到：{focus}")
    
    def _load_config_to_ui(self):
        """加载配置到 UI"""
        basic = self.config.basic_info
        self.unit_name_edit.setText(basic.unit_name)
        self.region_edit.setText(basic.region)
        self.well_name_edit.setText(basic.well_name)
        self.design_depth_edit.setText(f"{basic.design_depth_value} {basic.design_depth_unit}")
        
        contact = self.config.contact_info
        self.comm_status_edit.setText(contact.communication_status)
        self.manager_phone_edit.setText(contact.manager_phone)
        self.thuraya_phone_edit.setText(contact.thuraya_phone)
        self.security_status_edit.setText(contact.security_status)
        
        # 加载工况词条
        self._load_tokens()
        
        # 更新人员信息标签
        snapshot = self.report_service.calculate_personnel_snapshot()
        self.personnel_info_label.setText(
            f"中方{snapshot.chinese_total}人，当地雇员{snapshot.local_foreign_total}人"
        )
    
    def _load_tokens(self):
        """加载工况词条"""
        # 清除现有词条
        while self.tokens_layout.count():
            item = self.tokens_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加词条按钮
        for token in sorted(self.config.operation_tokens, key=lambda x: x.sort_order):
            if not token.enabled:
                continue
            
            btn = QPushButton(token.text)
            btn.clicked.connect(lambda checked, t=token.text: self._add_token(t))
            self.tokens_layout.addWidget(btn)
    
    def _add_token(self, token_text):
        """添加工况词条"""
        if self.last_focused_operation == 'today':
            current = self.today_work_edit.toPlainText()
            if current and not current.endswith(','):
                current += ','
            self.today_work_edit.setPlainText(current + token_text)
        else:
            current = self.next_work_edit.toPlainText()
            if current and not current.endswith(','):
                current += ','
            self.next_work_edit.setPlainText(current + token_text)
    
    def _generate_report(self):
        """生成报表"""
        try:
            data = self._collect_data()
            report_text = self.report_service.generate_report(data)
            
            self.preview_dialog = QTextEdit()
            self.preview_dialog.setPlainText(report_text)
            self.preview_dialog.setReadOnly(True)
            self.preview_dialog.setWindowTitle('📄 报表预览')
            self.preview_dialog.resize(600, 400)
            self.preview_dialog.show()
            
            logger.info("报表已生成")
        except Exception as e:
            logger.error(f"生成报表失败：{e}")
            QMessageBox.critical(self, '错误', f'生成报表失败：{e}')
    
    def _collect_data(self) -> DailyReportData:
        """收集数据"""
        design_depth = self.design_depth_edit.text().split()
        depth_value = int(design_depth[0]) if design_depth else 0
        depth_unit = design_depth[1] if len(design_depth) > 1 else 'm'
        
        return DailyReportData(
            unit_name=self.unit_name_edit.text(),
            report_date=self.date_edit.date().toString('yyyy.MM.dd'),
            region=self.region_edit.text(),
            personnel_snapshot=self.report_service.calculate_personnel_snapshot(),
            supply_days=self.config.basic_info.supply_days_default,
            diesel_volume=self.config.basic_info.diesel_volume_default,
            diesel_days=self.config.basic_info.diesel_days_default,
            well_name=self.well_name_edit.text(),
            design_depth_value=depth_value,
            design_depth_unit=depth_unit,
            today_operations_text=self.today_work_edit.toPlainText(),
            current_depth=int(self.current_depth_edit.text() or 0),
            next_operations_text=self.next_work_edit.toPlainText(),
            communication_status=self.comm_status_edit.text(),
            manager_phone=self.manager_phone_edit.text(),
            thuraya_phone=self.thuraya_phone_edit.text(),
            sat_phone_internal=self.config.contact_info.sat_phone_internal,
            sat_phone_external=self.config.contact_info.sat_phone_external,
            security_status=self.security_status_edit.text()
        )
    
    def _copy_to_clipboard(self):
        """复制到剪贴板"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        
        if hasattr(self, 'preview_dialog'):
            clipboard.setText(self.preview_dialog.toPlainText())
            QMessageBox.information(self, '成功', '报表已复制到剪贴板')
        else:
            self._generate_report()
            if hasattr(self, 'preview_dialog'):
                clipboard.setText(self.preview_dialog.toPlainText())
                QMessageBox.information(self, '成功', '报表已复制到剪贴板')
    
    def _preview_report(self):
        """预览报表"""
        self._generate_report()
    
    def _show_wizard(self):
        """显示向导"""
        dialog = WizardDialog(self, self.config_service)
        if dialog.exec():
            self.config = self.config_service.config
            self.report_service.config = self.config
            self._load_config_to_ui()
    
    def _manage_personnel(self):
        """管理人员"""
        QMessageBox.information(self, '提示', '人员管理功能开发中...')
    
    def _manage_tokens(self):
        """管理工况词条"""
        QMessageBox.information(self, '提示', '工况词条管理功能开发中...')
    
    def _export_txt(self):
        """导出 TXT"""
        QMessageBox.information(self, '提示', '导出功能开发中...')
    
    def _new_report(self):
        """新建报表"""
        self.today_work_edit.clear()
        self.next_work_edit.clear()
        self.current_depth_edit.clear()
    
    def _show_help(self):
        """显示帮助"""
        help_text = """
🛢 每日报表生成器 使用说明

1. 填写基础信息（单位、日期、井号等）
2. 点击工况词条自动添加到当前焦点输入框
3. 点击"生成报表"预览
4. 点击"复制到剪贴板"复制

快捷键:
- 点击今日工况框，词条添加到今日工况
- 点击下步工况框，词条添加到下步工况

配置保存在：
%APPDATA%\\DailyReportApp\\config.json
        """
        QMessageBox.information(self, '使用说明', help_text)
    
    def _show_about(self):
        """显示关于"""
        about_text = """
🛢 每日报表生成器
版本：v5.0.0

By Freely QQ:20721
Pzxsky@Gmail.com

© 2026 All Rights Reserved.
        """
        QMessageBox.information(self, '关于', about_text)
