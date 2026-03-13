# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
import os

block_cipher = None

# 方法 1：明确列出所有需要的隐藏导入（解决模块导入问题）
hiddenimports = [
    'report_app',
    'report_app.services',
    'report_app.services.config_service',
    'report_app.ui',
    'report_app.ui.main_window_tk',
    'report_app.ui.wizard_window_tk',
    'pyperclip',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'datetime',
    'pathlib',
    'json',
    'logging',
]

# 方法 2：收集所有子模块（确保不遗漏）
hiddenimports += collect_submodules("report_app")

# 收集数据文件和二进制文件（使用 collect_all 的变通方法）
# 由于 collect_all 在 Analysis 前可能失败，我们手动收集
datas = []
binaries = []

# 收集 tkinter 数据
try:
    from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
    datas += collect_data_files('tkinter')
    datas += collect_data_files('PIL')
    binaries += collect_dynamic_libs('tkinter')
except:
    pass

# 图标路径
icon_path = 'resources/app_icon.ico'
if os.path.exists(icon_path):
    icon_list = [icon_path]
else:
    icon_list = []

a = Analysis(
    ['app.py'],
    pathex=['.', 'report_app', 'report_app/ui', 'report_app/services'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DailyReport',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_list,
)
