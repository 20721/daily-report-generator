# 🛢️ 钻井日报生成器

石油钻井日报快速生成工具 - 减少手动输入，一键生成标准格式日报。

## 📸 功能特点

- ✅ 所有字段可点选或下拉，减少手动输入
- ✅ 单位名称、区域、井号、设计井深可自定义并保存
- ✅ 人员情况按分组显示（919 队、厨师、大夫、顶驱、运输等）
- ✅ 今日工况/下步工况提供常用词条库，可点选组合
- ✅ 柴油量和可用天数自动计算
- ✅ 一键生成标准格式文本
- ✅ 自动复制到剪贴板
- ✅ 支持导出 txt 文件

## 📦 下载安装

### 方式 1：从 Release 下载（推荐）

1. 访问 [Releases 页面](https://github.com/20721/daily-report-generator/releases)
2. 下载最新的 `.exe` 安装包
3. 运行安装程序完成安装

### 方式 2：手动触发云编译

1. 进入 [Actions 页面](https://github.com/20721/daily-report-generator/actions)
2. 点击 "Build Windows App" 工作流
3. 点击 "Run workflow" 按钮
4. 等待编译完成（约 3-5 分钟）
5. 在下方 "Artifacts" 中下载 `daily-report-generator-windows.zip`

## 🚀 本地开发

```bash
# 克隆仓库
git clone https://github.com/20721/daily-report-generator.git
cd daily-report-generator

# 安装依赖
npm install

# 启动开发模式
npm start

# 本地打包测试
npm run build
```

## 📁 项目结构

```
daily-report-generator/
├── src/
│   ├── main.js          # Electron 主进程
│   ├── index.html       # 界面 HTML
│   ├── styles.css       # 样式
│   └── renderer.js      # 渲染进程逻辑
├── config.json          # 默认配置模板
├── package.json         # 项目配置
└── .github/workflows/
    └── build.yml        # GitHub Actions 编译配置
```

## ⚙️ 配置说明

首次运行时会自动创建配置文件，位置：
- Windows: `%APPDATA%\daily-report-generator\config.json`

可自定义配置：
- 单位名称、区域、井号
- 人员分组默认人数
- 工况词条库
- 通讯信息模板

## 📝 使用流程

1. 打开应用，日期默认为今天
2. 选择或修改基本信息（单位、井号等）
3. 调整人员数量（数字调节器）
4. 点选今日工况和下步工况
5. 输入柴油量和可用天数
6. 点击"生成日报"预览
7. 点击"复制到剪贴板"或"导出 TXT"

## 🔄 发布新版本

```bash
# 修改 package.json 版本号
# 提交并推送
git commit -am "v1.0.1 - 更新说明"
git tag v1.0.1
git push origin v1.0.1
```

推送 tag 后会自动触发编译并上传到 Release。

## 📄 许可证

MIT License

## 👤 作者

瓶子 <pzxsky@gmail.com>
