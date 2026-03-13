# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# 关键修复：使用 Analysis 的 pathex 参数，让 PyInstaller 能找到 report_app
a = Analysis(
    ['app.py'],
    pathex=['.', 'report_app', 'report_app/ui', 'report_app/services'],
    binaries=[],
    datas=[],
    hiddenimports=[
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
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 在 Analysis 之后，手动添加 report_app 的所有子模块
try:
    from PyInstaller.utils.hooks import collect_submodules
    a.hiddenimports += collect_submodules("report_app")
    print("Added submodules from report_app")
except Exception as e:
    print("Warning: Could not collect submodules: " + str(e))

# 图标路径
icon_path = 'resources/app_icon.ico'
if os.path.exists(icon_path):
    icon_list = [icon_path]
else:
    icon_list = []

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
