"""配置服务 - 负责配置读写"""
import json
import os
from pathlib import Path
from datetime import datetime
from report_app.models.config_models import AppConfig, BasicInfoConfig
from report_app.utils.paths import get_config_dir, get_config_path
from report_app.utils.logger import get_logger

logger = get_logger()


class ConfigService:
    def __init__(self):
        self.config_path = get_config_path()
        self.config: AppConfig = None
        self.default_config = self._get_default_config()
    
    def _get_default_config(self) -> AppConfig:
        """获取默认配置"""
        return AppConfig(
            basic_info=BasicInfoConfig(),
            personnel_items=self._get_default_personnel(),
            contact_info=self._get_default_contact(),
            operation_tokens=self._get_default_tokens()
        )
    
    def _get_default_personnel(self):
        """默认人员模块"""
        return [
            {"id": "unit_chinese", "name": "919 队", "category_tag": "chinese", "count": 14,
             "include_in_bracket_detail": True, "include_in_chinese_total": True,
             "include_in_local_total": False, "sort_order": 10, "enabled": True,
             "special_title": "", "special_name": "", "special_action": ""},
            {"id": "cook", "name": "外聘厨师", "category_tag": "chinese", "count": 3,
             "include_in_bracket_detail": True, "include_in_chinese_total": True,
             "include_in_local_total": False, "sort_order": 20, "enabled": True,
             "special_title": "", "special_name": "", "special_action": ""},
            {"id": "local", "name": "919 队当地雇员", "category_tag": "local_foreign", "count": 29,
             "include_in_bracket_detail": False, "include_in_chinese_total": False,
             "include_in_local_total": True, "sort_order": 10, "enabled": True,
             "special_title": "", "special_name": "", "special_action": ""},
            {"id": "soldier", "name": "士兵", "category_tag": "local_foreign", "count": 8,
             "include_in_bracket_detail": False, "include_in_chinese_total": False,
             "include_in_local_total": True, "sort_order": 20, "enabled": True,
             "special_title": "", "special_name": "", "special_action": ""},
            {"id": "manager", "name": "基地经理", "category_tag": "special", "count": 1,
             "include_in_bracket_detail": True, "include_in_chinese_total": True,
             "include_in_local_total": False, "sort_order": 100, "enabled": True,
             "special_title": "基地经理", "special_name": "赵铁寨", "special_action": "驻井指导工作"},
        ]
    
    def _get_default_contact(self):
        """默认通讯信息"""
        return {
            "communication_status": "当地手机信号差",
            "manager_phone": "00235-93577318",
            "thuraya_phone": "008821621906786",
            "sat_phone_internal": "6660353（内线）",
            "sat_phone_external": "021-80246760（外线）",
            "security_status": "周边安全无异常"
        }
    
    def _get_default_tokens(self):
        """默认工况词条"""
        return [
            {"id": "t1", "text": "下套管", "sort_order": 10, "enabled": True},
            {"id": "t2", "text": "循环", "sort_order": 20, "enabled": True},
            {"id": "t3", "text": "固井", "sort_order": 30, "enabled": True},
            {"id": "t4", "text": "候凝", "sort_order": 40, "enabled": True},
            {"id": "t5", "text": "安装套管头", "sort_order": 50, "enabled": True},
            {"id": "t6", "text": "安装 BOP", "sort_order": 60, "enabled": True},
            {"id": "t7", "text": "试压", "sort_order": 70, "enabled": True},
            {"id": "t8", "text": "BOP 试压", "sort_order": 80, "enabled": True},
            {"id": "t9", "text": "组合二开钻具", "sort_order": 90, "enabled": True},
            {"id": "t10", "text": "下钻", "sort_order": 100, "enabled": True},
            {"id": "t11", "text": "钻塞", "sort_order": 110, "enabled": True},
            {"id": "t12", "text": "二开钻进", "sort_order": 120, "enabled": True},
        ]
    
    def load(self) -> AppConfig:
        """加载配置"""
        try:
            if not self.config_path.exists():
                logger.info("配置文件不存在，使用默认配置")
                self.config = self.default_config
                return self.config
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.config = AppConfig(**data)
                logger.info(f"配置已加载：{self.config_path}")
                return self.config
        except Exception as e:
            logger.error(f"加载配置失败：{e}")
            self.config = self.default_config
            return self.config
    
    def save(self, config: AppConfig) -> bool:
        """保存配置"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 备份旧配置
            if self.config_path.exists():
                backup_path = self.config_path.parent / f"config.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.config_path.rename(backup_path)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config.model_dump(), f, ensure_ascii=False, indent=2)
            
            self.config = config
            logger.info(f"配置已保存：{self.config_path}")
            return True
        except Exception as e:
            logger.error(f"保存配置失败：{e}")
            return False
    
    def has_config(self) -> bool:
        """检查是否有配置"""
        return self.config_path.exists()
    
    def reset_to_default(self) -> bool:
        """重置为默认配置"""
        return self.save(self.default_config)
