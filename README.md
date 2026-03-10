# 🛢️ 钻井日报生成器

石油钻井日报快速生成工具 - 减少手动输入，一键生成标准格式日报。

## 📥 下载安装

### 方法 1：从 Release 下载（推荐）
1. 访问 [Releases 页面](https://github.com/20721/daily-report-generator/releases)
2. 下载最新的 `.exe` 安装包
3. 双击安装即可使用

### 方法 2：自行编译
```bash
git clone https://github.com/20721/daily-report-generator.git
cd daily-report-generator
npm install
npm run build
```

## 🚀 自动编译触发

### 触发方式 1：创建 Tag（生成 Release）
```bash
git tag v1.0.0
git push origin v1.0.0
```
编译完成后，在 Releases 页面下载 `.exe` 安装包。

### 触发方式 2：手动触发
1. 访问 [Actions](https://github.com/20721/daily-report-generator/actions)
2. 点击 "Build Windows Executable"
3. 点击 "Run workflow"
4. 编译完成后在 Artifacts 下载

## 📖 使用说明

### 基本字段
- **单位名称/区域/井号/设计井深**：可自定义，自动保存
- **日期**：默认今天，可修改
- **当前井深**：可选填

### 人员情况
- 按分组显示数字调节器（919 队、厨师、大夫、顶驱、运输、固井、基地经理、当地雇员、士兵、安保）
- 基地经理可设置是否驻井

### 工况选择
- **今日工况**：从词条库点选，支持自定义添加
- **下步工况**：从词条库点选，支持自定义添加
- 常用工况已预置（一开验收、钻进、循环、起钻、下套管等）

### 物资情况
- 生活物资储备天数
- 柴油量和可用天数（数字输入）

### 输出功能
- **生成日报**：预览标准格式文本
- **复制到剪贴板**：一键复制，可直接粘贴到微信/邮件
- **导出 TXT**：保存为文本文件
- **保存配置**：保存自定义设置到本地

## 📁 项目结构

```
daily-report-generator/
├── src/
│   ├── main.js          # Electron 主进程
│   ├── index.html       # 界面
│   ├── styles.css       # 样式
│   └── renderer.js      # 渲染进程逻辑
├── .github/
│   └── workflows/
│       └── build.yml    # GitHub Actions 编译配置
├── config.json          # 默认配置模板
├── package.json         # 项目配置
└── README.md            # 说明文档
```

## 🔧 技术栈

- Electron 28
- HTML/CSS/JavaScript
- GitHub Actions (云编译)
- NSIS (Windows 安装包)

## 📝 配置说明

首次运行时会自动创建配置文件，位置：
- Windows: `%APPDATA%\com.bottle.dailyreport\config.json`

配置项包括：
- 单位基本信息
- 人员分组默认值
- 工况词条库
- 通讯信息模板

## 📄 输出格式示例

```
1.单位名称：Rig919
2.日期：2026.03.10
3.所在区域：H
4.人员情况：中方人员 35 人（其中 919 队 14 人，厨师 3 人，大夫 2 人...）
5.生活物资储备天数：30 天；井场柴油 53 方，可用 13 天。
6.井号：Raphia SW1-22 设计井深：1086 m
7.今日工况：一开验收，整改，组合 BHA，技术交底，一开钻进。
8.当前井深：136 m
9.下步工况：一开钻进，循环，短起下，循环，起钻，下套管。
10.通讯情况：当地手机信号差，平台经理：00235-93577318...
11.安全情况：周边安全无异常
```

## 📞 联系方式

作者：瓶子 <pzxsky@gmail.com>

## 📜 许可证

MIT License
