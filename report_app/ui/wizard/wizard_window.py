"""首次运行向导窗口"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                QLineEdit, QPushButton, QSpinBox, QFrame,
                                QStackedWidget, QWidget, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from report_app.utils.logger import get_logger

logger = get_logger()


class WizardDialog(QDialog):
    def __init__(self, parent, config_service):
        super().__init__(parent)
        self.config_service = config_service
        self.config = config_service.config
        
        self.setWindowTitle('🎉 欢迎使用每日报表生成器 - 首次配置向导')
        self.setMinimumSize(700, 550)
        self.setModal(True)
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        
        # 进度标签
        self.progress_label = QLabel('第 1 页 / 共 3 页')
        self.progress_label.setFont(QFont('Microsoft YaHei UI', 10))
        layout.addWidget(self.progress_label)
        
        # 页面栈
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # 创建页面
        self._create_page1()
        self._create_page2()
        self._create_page3()
        
        # 按钮区
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.prev_btn = QPushButton('上一步')
        self.prev_btn.clicked.connect(self._prev_page)
        self.prev_btn.setEnabled(False)
        btn_layout.addWidget(self.prev_btn)
        
        self.next_btn = QPushButton('下一步')
        self.next_btn.clicked.connect(self._next_page)
        btn_layout.addWidget(self.next_btn)
        
        layout.addLayout(btn_layout)
    
    def _create_page1(self):
        """第 1 页：基础信息"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel('📋 基础信息')
        title.setFont(QFont('Microsoft YaHei UI', 14, QFont.Bold))
        layout.addWidget(title)
        
        layout.addWidget(QLabel('单位名称:'))
        self.unit_name_edit = QLineEdit(self.config.basic_info.unit_name)
        layout.addWidget(self.unit_name_edit)
        
        layout.addWidget(QLabel('所在区域:'))
        self.region_edit = QLineEdit(self.config.basic_info.region)
        layout.addWidget(self.region_edit)
        
        layout.addWidget(QLabel('井号:'))
        self.well_name_edit = QLineEdit(self.config.basic_info.well_name)
        layout.addWidget(self.well_name_edit)
        
        layout.addWidget(QLabel('设计井深 (m):'))
        self.design_depth_spin = QSpinBox()
        self.design_depth_spin.setRange(0, 20000)
        self.design_depth_spin.setValue(self.config.basic_info.design_depth_value)
        layout.addWidget(self.design_depth_spin)
        
        layout.addStretch()
        self.stack.addWidget(page)
    
    def _create_page2(self):
        """第 2 页：人员初始化"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel('👥 人员初始化')
        title.setFont(QFont('Microsoft YaHei UI', 14, QFont.Bold))
        layout.addWidget(title)
        
        layout.addWidget(QLabel('本单位中方人数:'))
        self.unit_chinese_spin = QSpinBox()
        self.unit_chinese_spin.setRange(0, 500)
        self.unit_chinese_spin.setValue(14)
        layout.addWidget(self.unit_chinese_spin)
        
        layout.addWidget(QLabel('外聘厨师人数:'))
        self.cook_spin = QSpinBox()
        self.cook_spin.setRange(0, 50)
        self.cook_spin.setValue(3)
        layout.addWidget(self.cook_spin)
        
        layout.addWidget(QLabel('本单位当地雇员人数:'))
        self.local_spin = QSpinBox()
        self.local_spin.setRange(0, 500)
        self.local_spin.setValue(29)
        layout.addWidget(self.local_spin)
        
        layout.addWidget(QLabel('士兵人数:'))
        self.soldier_spin = QSpinBox()
        self.soldier_spin.setRange(0, 100)
        self.soldier_spin.setValue(8)
        layout.addWidget(self.soldier_spin)
        
        layout.addWidget(QLabel('基地经理姓名:'))
        self.manager_name_edit = QLineEdit('赵铁寨')
        layout.addWidget(self.manager_name_edit)
        
        layout.addStretch()
        self.stack.addWidget(page)
    
    def _create_page3(self):
        """第 3 页：通讯信息"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel('📞 通讯信息')
        title.setFont(QFont('Microsoft YaHei UI', 14, QFont.Bold))
        layout.addWidget(title)
        
        layout.addWidget(QLabel('平台经理电话:'))
        self.manager_phone_edit = QLineEdit(self.config.contact_info.manager_phone)
        layout.addWidget(self.manager_phone_edit)
        
        layout.addWidget(QLabel('Thuraya 电话:'))
        self.thuraya_phone_edit = QLineEdit(self.config.contact_info.thuraya_phone)
        layout.addWidget(self.thuraya_phone_edit)
        
        layout.addWidget(QLabel('通讯情况默认文本:'))
        self.comm_status_edit = QLineEdit(self.config.contact_info.communication_status)
        layout.addWidget(self.comm_status_edit)
        
        layout.addWidget(QLabel('安全情况默认文本:'))
        self.security_status_edit = QLineEdit(self.config.contact_info.security_status)
        layout.addWidget(self.security_status_edit)
        
        layout.addStretch()
        self.stack.addWidget(page)
    
    def _next_page(self):
        """下一页"""
        current = self.stack.currentIndex()
        if current < self.stack.count() - 1:
            self.stack.setCurrentIndex(current + 1)
            self.progress_label.setText(f'第 {current + 2} 页 / 共 {self.stack.count()} 页')
            self.prev_btn.setEnabled(True)
            
            if current == self.stack.count() - 2:
                self.next_btn.setText('完成')
        else:
            self._finish()
    
    def _prev_page(self):
        """上一页"""
        current = self.stack.currentIndex()
        if current > 0:
            self.stack.setCurrentIndex(current - 1)
            self.progress_label.setText(f'第 {current} 页 / 共 {self.stack.count()} 页')
            
            if current == 1:
                self.prev_btn.setEnabled(False)
            
            if self.next_btn.text() == '完成':
                self.next_btn.setText('下一步')
    
    def _finish(self):
        """完成向导"""
        # 保存配置
        self.config.basic_info.unit_name = self.unit_name_edit.text()
        self.config.basic_info.region = self.region_edit.text()
        self.config.basic_info.well_name = self.well_name_edit.text()
        self.config.basic_info.design_depth_value = self.design_depth_spin.value()
        
        # 更新人员配置
        for item in self.config.personnel_items:
            if item.id == 'unit_chinese':
                item.count = self.unit_chinese_spin.value()
            elif item.id == 'cook':
                item.count = self.cook_spin.value()
            elif item.id == 'local':
                item.count = self.local_spin.value()
            elif item.id == 'soldier':
                item.count = self.soldier_spin.value()
            elif item.id == 'manager':
                item.special_name = self.manager_name_edit.text()
        
        # 更新通讯信息
        self.config.contact_info.manager_phone = self.manager_phone_edit.text()
        self.config.contact_info.thuraya_phone = self.thuraya_phone_edit.text()
        self.config.contact_info.communication_status = self.comm_status_edit.text()
        self.config.contact_info.security_status = self.security_status_edit.text()
        
        # 保存配置
        if self.config_service.save(self.config):
            QMessageBox.information(self, '完成', '配置已保存！\n\n现在可以开始使用每日报表生成器了。')
            logger.info("向导完成，配置已保存")
            self.accept()
        else:
            QMessageBox.critical(self, '错误', '保存配置失败！')
