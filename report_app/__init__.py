"""report_app 包"""
__version__ = '1.0.0'

# 显式导入子模块，确保 PyInstaller 能正确收集
from . import services
from . import ui
from . import models
from . import utils
