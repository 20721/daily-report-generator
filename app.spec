# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

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
        'report_app.models',
        'report_app.models.config_models',
        'pyperclip',
        'pydantic',
        'pydantic_core',
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
