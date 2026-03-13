# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all, collect_submodules
import os

block_cipher = None

# 收集 report_app 所有子模块
datas = []
binaries = []
hiddenimports = []

# 关键修复：使用 collect_all 收集包的所有内容
try:
    tmp = collect_all("report_app")
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]
except Exception as e:
    print(f"Warning: collect_all failed: {e}")

# 收集所有子模块（确保不遗漏）
hiddenimports += collect_submodules("report_app")

# 添加其他依赖
hiddenimports += ['pyperclip', 'json', 'os', 'sys', 'pathlib', 'datetime', 'tkinter']

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
