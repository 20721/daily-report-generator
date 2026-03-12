"""日志工具"""
import logging
from pathlib import Path

_logger = None


def setup_logger() -> logging.Logger:
    """设置日志"""
    global _logger
    
    if _logger:
        return _logger
    
    from .paths import get_logs_dir
    log_dir = get_logs_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"{Path.home().name}_{Path.cwd().name}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    _logger = logging.getLogger('DailyReport')
    return _logger


def get_logger() -> logging.Logger:
    """获取日志实例"""
    global _logger
    if not _logger:
        _logger = logging.getLogger('DailyReport')
    return _logger
