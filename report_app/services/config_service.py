"""配置服务 - 负责配置读写和验证"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional


class ConfigValidationError(Exception):
    """配置验证异常"""
    pass


class ConfigService:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / 'config.json'
        self.config: Optional[Dict] = None
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def _get_config_dir(self) -> Path:
        """获取配置目录"""
        if os.name == 'nt':  # Windows
            appdata = os.environ.get('APPDATA', '')
            if appdata:
                return Path(appdata) / 'DailyReportApp'
        # Fallback 到程序目录
        if getattr(sys, 'frozen', False):
            return Path(os.path.dirname(sys.executable)) / 'config'
        return Path(__file__).parent.parent.parent / 'config'
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'version': '1.0',
            'fixed_fields': {
                'unit_name': '',
                'region': '',
                'well_name': '',
                'design_depth': 0,
                'supply_days': 30,
                'diesel_volume': 50,
                'diesel_days': 15
            },
            'personnel_modules': [],
            'work_tokens': {
                'all_tokens': [],
                'today': [],
                'next': []
            },
            'comm_info': {
                'status': '',
                'manager_phone': '',
                'thuraya_phone': '',
                'sat_internal': '',
                'sat_external': '',
                'security': ''
            },
            'current_data': {
                'date': datetime.now().strftime('%Y.%m.%d'),
                'current_depth': 0
            },
            'ui_prefs': {
                'count_range_min': 1,
                'count_range_max': 20
            }
        }
    
    def load(self) -> Tuple[bool, str]:
        """
        加载配置文件
        返回：(成功标志，错误信息)
        """
        try:
            if not self.config_file.exists():
                self.config = self._get_default_config()
                return True, '配置文件不存在，已创建默认配置'
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 验证配置
            is_valid, errors = self.validate_config()
            if not is_valid:
                return False, '配置文件验证失败：' + '; '.join(errors)
            
            return True, '配置加载成功'
        except json.JSONDecodeError as e:
            self.config = self._get_default_config()
            return False, f'配置文件格式错误：{str(e)}'
        except Exception as e:
            self.config = self._get_default_config()
            return False, f'加载配置失败：{str(e)}'
    
    def save(self) -> Tuple[bool, str]:
        """
        保存配置文件
        返回：(成功标志，错误信息)
        """
        try:
            # 保存前先验证
            is_valid, errors = self.validate_config()
            if not is_valid:
                return False, '配置验证失败：' + '; '.join(errors)
            
            # 创建目录
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # 备份旧配置
            if self.config_file.exists():
                backup_dir = self.config_dir / 'backups'
                backup_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = backup_dir / f'config.backup.{timestamp}.json'
                import shutil
                shutil.copy2(self.config_file, backup_path)
            
            # 保存新配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            # 创建必要文件夹
            (self.config_dir / 'reports').mkdir(parents=True, exist_ok=True)
            (self.config_dir / 'logs').mkdir(parents=True, exist_ok=True)
            (self.config_dir / 'backups').mkdir(parents=True, exist_ok=True)
            
            return True, '配置保存成功'
        except Exception as e:
            return False, f'保存配置失败：{str(e)}'
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """
        验证配置文件
        返回：(是否有效，错误列表)
        """
        errors = []
        
        if not self.config:
            errors.append('配置对象为空')
            return False, errors
        
        # 验证固定字段
        fixed = self.config.get('fixed_fields', {})
        if not fixed.get('unit_name'):
            errors.append('单位名称不能为空')
        if not fixed.get('region'):
            errors.append('所在区域不能为空')
        if not fixed.get('well_name'):
            errors.append('井号不能为空')
        if fixed.get('design_depth', 0) <= 0:
            errors.append('设计井深必须大于 0')
        
        # 验证人员模块
        personnel = self.config.get('personnel_modules', [])
        if not personnel:
            errors.append('至少需要一个人员模块')
        else:
            labels = set()
            for i, module in enumerate(personnel):
                if not module.get('label'):
                    errors.append(f'人员模块 [{i+1}] 缺少标签')
                if module.get('count', 0) < 0:
                    errors.append(f'人员模块 [{module.get("label", i+1)}] 人数不能为负数')
                label = module.get('label', '')
                if label in labels:
                    errors.append(f'人员模块标签重复：{label}')
                labels.add(label)
        
        # 验证工况词条
        work_tokens = self.config.get('work_tokens', {}).get('all_tokens', [])
        if not work_tokens:
            errors.append('至少需要一个工况词条')
        
        # 验证通讯信息
        comm = self.config.get('comm_info', {})
        if not comm.get('status'):
            errors.append('通讯情况不能为空')
        if not comm.get('manager_phone'):
            errors.append('平台经理电话不能为空')
        if not comm.get('thuraya_phone'):
            errors.append('Thuraya 电话不能为空')
        if not comm.get('security'):
            errors.append('安全情况不能为空')
        
        return len(errors) == 0, errors
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        if not self.config:
            return default
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        if not self.config:
            self.config = self._get_default_config()
        self.config[key] = value
    
    def get_chinese_total(self) -> int:
        """计算中方人员总数"""
        total = 0
        for module in self.config.get('personnel_modules', []):
            if module.get('category') == 'chinese':
                total += module.get('count', 0)
        return total
    
    def get_local_total(self) -> int:
        """计算当地雇员总数"""
        total = 0
        for module in self.config.get('personnel_modules', []):
            if module.get('category') == 'local':
                total += module.get('count', 0)
        return total
    
    def has_config(self) -> bool:
        """检查是否有配置"""
        return self.config_file.exists() and self.config is not None
    
    def reset(self):
        """重置为默认配置"""
        self.config = self._get_default_config()
