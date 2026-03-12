"""路径工具 - 处理配置、日志等目录"""
import os
import sys
from pathlib import Path


def get_app_dir() -> Path:
    """获取程序目录"""
    if getattr(sys, 'frozen', False):
        return Path(os.path.dirname(sys.executable))
    return Path(__file__).parent.parent.parent


def get_config_dir() -> Path:
    """获取配置目录（优先使用 APPDATA）"""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('APPDATA', '')
        if appdata:
            return Path(appdata) / 'DailyReportApp'
    
    # fallback 到程序目录
    return get_app_dir() / 'config'


def get_config_path() -> Path:
    """获取配置文件路径"""
    return get_config_dir() / 'config.json'


def get_logs_dir() -> Path:
    """获取日志目录"""
    return get_config_dir() / 'logs'


def get_history_dir() -> Path:
    """获取历史记录目录"""
    return get_config_dir() / 'report_history'


def get_backups_dir() -> Path:
    """获取备份目录"""
    return get_config_dir() / 'backups'
