# 每日报表生成器 (Go+Walk 版)

**版本**: v6.1.1  
**平台**: Windows 10 / Windows 11  
**技术栈**: Go 1.21 + Walk GUI  
**文件大小**: ~5-8 MB (目标)

---

## 📋 项目简介

专为石油钻井行业设计的日报快速生成工具。

**v6.1.1 更新**:
- ✅ 使用 Walk 库 (Windows 原生 GUI)
- ✅ 目标文件大小 < 15MB
- ✅ Windows 原生 API

---

## 🔧 Walk 库版本

```
github.com/lxn/walk v0.0.0-20210112000159-7d2f8975554c
```

**来源**: https://pkg.go.dev/github.com/lxn/walk

---

## 🚀 快速开始

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
- `-H=windowsgui`: Windows GUI 模式

---

© 2026 All Rights Reserved.
