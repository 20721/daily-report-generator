# 每日报表生成器 (Tkinter 轻量版)

**版本**: v5.1.0  
**平台**: Windows 10 / Windows 11  
**技术栈**: Python 3.12 + Tkinter + PyInstaller  
**文件大小**: ~12 MB (轻量级)

---

## 📋 项目简介

专为石油钻井行业设计的日报快速生成工具。

**v5.1.0 更新**:
- ✅ 改用 Tkinter GUI (大幅减小文件体积)
- ✅ 文件大小从 52MB 降至~12MB
- ✅ 修复 PySide6 导入错误
- ✅ 保持所有核心功能不变

---

## 🚀 快速开始

### 直接使用 EXE

1. 下载 `output/DailyReport.exe`
2. 双击运行
3. 首次运行自动弹出配置向导

### 从源码运行

```bash
# 1. 克隆项目
git clone https://github.com/20721/daily-report-generator.git
cd daily-report-generator

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行程序
python app.py
```

---

## 📦 构建 EXE

### Windows

```bash
build_exe.bat
```

或手动执行:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name DailyReport app.py
```

---

## ⚙️ 配置说明

### 配置位置

```
%APPDATA%\DailyReportApp\config.json
```

### 配置内容

- 基础信息（单位、井号、设计井深等）
- 人员模块（中方/外籍/特殊说明）
- 通讯信息（电话、安全情况等）
- 工况词条（可自定义）

---

## 📝 使用说明

### 首次运行

1. 启动程序后自动弹出配置向导
2. 填写基础信息
3. 配置人员数量
4. 填写通讯信息
5. 完成配置，进入主界面

### 日常使用

1. 确认日期（默认当天）
2. 填写当前井深
3. 点击工况词条添加到"今日工况"或"下步工况"
4. 点击"生成报表"预览
5. 点击"复制到剪贴板"

### 工况词条焦点

- 点击"今日工况"输入框 → 词条添加到今日工况
- 点击"下步工况"输入框 → 词条添加到下步工况

---

## 📤 功能列表

- ✅ 首次运行设置向导
- ✅ 全中文 Tkinter 界面
- ✅ 模块化人员配置
- ✅ 工况词条管理（点击添加到焦点）
- ✅ 报表生成和复制
- ✅ 单文件 EXE 发布 (~12MB)
- ✅ 自动保存配置
- ✅ 配置保存到 %APPDATA%

---

## 🔧 故障排除

### 程序无法启动

1. 删除 `%APPDATA%\DailyReportApp\config.json` 重置配置
2. 查看日志文件：`%APPDATA%\DailyReportApp\logs\`

### 配置保存失败

1. 检查磁盘空间
2. 检查 `%APPDATA%` 目录权限

---

## 📞 联系信息

**开发者**: Freely (瓶子)  
**QQ**: 20721  
**Email**: pzxsky@gmail.com  
**GitHub**: https://github.com/20721/daily-report-generator

---

## 📄 许可证

© 2026 All Rights Reserved.

---

*最后更新：2026-03-13*
