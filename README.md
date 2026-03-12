# 每日报表生成器 (Go+Walk 版)

**版本**: v6.1.0  
**平台**: Windows 10 / Windows 11  
**技术栈**: Go 1.21 + Walk GUI  
**文件大小**: ~5-8 MB

---

## 📋 项目简介

专为石油钻井行业设计的日报快速生成工具。

**v6.1.0 更新**:
- ✅ 使用 Go + Walk（Windows 原生 GUI）
- ✅ 文件大小约 5-8MB
- ✅ Windows 原生 API，无 OpenGL 依赖
- ✅ 编译速度快

---

## 🚀 快速开始

### 直接使用 EXE

1. 下载 `output/report.exe`
2. 双击运行

### 从源码编译

```bash
cd cmd/report
go build -ldflags="-s -w -H=windowsgui" -o report.exe .
```

---

## 📦 构建 EXE

```bash
go build -ldflags="-s -w -H=windowsgui" -o output/report.exe ./cmd/report
```

### 优化选项

- `-s`: 剥离符号表
- `-w`: 剥离 DWARF 调试信息
- `-H=windowsgui`: Windows GUI 模式（无控制台窗口）

---

© 2026 All Rights Reserved.
