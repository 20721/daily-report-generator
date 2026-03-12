"""配置数据模型"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class BasicInfoConfig(BaseModel):
    """基础信息配置"""
    unit_name: str = "Rig919"
    region: str = "H"
    well_name: str = ""
    design_depth_value: int = 1000
    design_depth_unit: str = "m"
    supply_days_default: int = 30
    diesel_volume_default: int = 50
    diesel_days_default: int = 15


class PersonnelItemConfig(BaseModel):
    """人员模块配置"""
    id: str
    name: str
    category_tag: str  # chinese / local_foreign / special
    count: int = 0
    include_in_bracket_detail: bool = True
    include_in_chinese_total: bool = False
    include_in_local_total: bool = False
    special_title: str = ""
    special_name: str = ""
    special_action: str = ""
    sort_order: int = 0
    enabled: bool = True


class ContactInfoConfig(BaseModel):
    """通讯信息配置"""
    communication_status: str = "通讯正常"
    manager_phone: str = ""
    thuraya_phone: str = ""
    sat_phone_internal: str = ""
    sat_phone_external: str = ""
    security_status: str = "安全无异常"


class OperationTokenConfig(BaseModel):
    """工况词条配置"""
    id: str
    text: str
    sort_order: int = 0
    enabled: bool = True


class UiPreferenceConfig(BaseModel):
    """UI 偏好配置"""
    window_width: int = 1280
    window_height: int = 820
    theme: str = "light"


class AppConfig(BaseModel):
    """主配置模型"""
    config_version: int = 1
    basic_info: BasicInfoConfig = Field(default_factory=BasicInfoConfig)
    personnel_items: List[PersonnelItemConfig] = Field(default_factory=list)
    contact_info: ContactInfoConfig = Field(default_factory=ContactInfoConfig)
    operation_tokens: List[OperationTokenConfig] = Field(default_factory=list)
    ui_prefs: UiPreferenceConfig = Field(default_factory=UiPreferenceConfig)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d')
        }
