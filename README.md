# 每日报表生成器 (Go 语言版)

**版本**: v6.0.0  
**平台**: Windows 10 / Windows 11  
**技术栈**: Go 1.21 + Fyne GUI  
**文件大小**: ~10 MB (轻量级)

---

## 📋 项目简介

专为石油钻井行业设计的日报快速生成工具。

**v6.0.0 更新**:
- ✅ 使用 Go 语言重写（无 Python 依赖）
- ✅ Fyne GUI 跨平台界面
- ✅ 文件大小约 10MB（符合<15MB 要求）
- ✅ 单文件 EXE，无运行时依赖
- ✅ Windows 原生运行

---

## 🚀 快速开始

### 直接使用 EXE

1. 下载 `output/report.exe`
2. 双击运行
3. 首次运行自动弹出配置向导

### 从源码编译

```bash
# 1. 克隆项目
git clone https://github.com/20721/daily-report-generator.git
cd daily-report-generator

# 2. 安装依赖
go mod download

# 3. 编译
cd cmd/report
go build -ldflags="-s -w" -o report.exe .

# 4. 运行
./report.exe
```

---

## 📦 构建 EXE

### Windows

```bash
cd cmd/report
go build -ldflags="-s -w" -o ../../output/report.exe .
```

### 优化选项

- `-s`: 剥离符号表
- `-w`: 剥离 DWARF 调试信息
- 可减小约 30% 文件大小

---

## ⚙️ 配置说明

### 配置位置

```
%APPDATA%\DailyReportApp\config.json
```

---

## 📝 使用说明

### 首次运行

1. 启动程序后自动弹出配置向导
2. 填写基础信息
3. 完成配置，进入主界面

### 日常使用

1. 确认日期（默认当天）
2. 填写当前井深
3. 点击工况词条添加到"今日工况"或"下步工况"
4. 点击"生成报表"预览
5. 点击"复制到剪贴板"

---

## 📤 功能列表

- ✅ 首次运行设置向导
- ✅ 全中文 Fyne GUI 界面
- ✅ 模块化人员配置
- ✅ 工况词条管理
- ✅ 报表生成和复制
- ✅ 单文件 EXE 发布 (~10MB)
- ✅ 自动保存配置
- ✅ 无运行时依赖

---

## 🔧 技术栈

- **语言**: Go 1.21+
- **GUI**: Fyne v2.4.3
- **打包**: go build -ldflags="-s -w"
- **目标**: Windows 10/11 原生 EXE

---

## 📞 联系信息

**开发者**: Freely (瓶子)  
**QQ**: 20721  
**Email**: pzxsky@gmail.com  
**GitHub**: https://github.com/20721/daily-report-generator

---

© 2026 All Rights Reserved.
