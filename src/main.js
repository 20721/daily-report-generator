const { app, BrowserWindow, ipcMain, clipboard, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;
const configPath = path.join(app.getPath('userData'), 'config.json');

function loadConfig() {
  try {
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    }
  } catch (e) { console.error('加载配置失败:', e); }
  return getDefaultConfig();
}

function saveConfig(config) {
  try {
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    return true;
  } catch (e) { console.error('保存配置失败:', e); return false; }
}

function getDefaultConfig() {
  return {
    unitName: 'Rig919',
    area: 'H',
    wellName: 'Raphia SW1-22',
    designDepth: '1086',
    staffGroups: {
      '919 队': 14, '厨师': 3, '大夫': 2, '顶驱': 1,
      '运输': 11, '固井': 3, '基地经理': 1,
      '当地雇员': 29, '士兵': 8, '安保': 13
    },
    manager: '赵铁寨',
    phone: '00235-93577318',
    thuraya: '008821621906786',
    satInternal: '6660353',
    satExternal: '021-80246760',
    workConditions: [
      '一开验收', '整改', '组合 BHA', '技术交底', '一开钻进',
      '循环', '短起下', '起钻', '下套管', '组合钻具',
      '配一开泥浆', '自查自改', '井场标准化', '测试顶驱',
      '铺井场设备围堰', '上钻具', '钻具通径', '安装导管喇叭口',
      '起井架底座', '安装飘台', '安装顶驱导轨', '挂顶驱', '安装顶驱',
      '远控房及液压管排就位', '安装立管阀门组', '安装放喷管线',
      '安装天车', '穿引绳', '穿大绳', '安装逃生绳', '安装动力绳',
      '安装死活绳头', '起井架', '安装固控设备', '安装泥浆罐',
      '拆转盘', '拆大梁', '拆底座拉筋', '拆底座', '清理钢木基础',
      '搬迁井架', '搬迁泥浆罐', '搬迁水罐', '铺钢木基础',
      '憋压侯凝', '座套管卡瓦', '甩 BOP 组', '安装油管头', '安装采油树',
      '甩钻具', '下套管', '固井', '电测', '二开钻进'
    ],
    nextConditions: []
  };
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => app.quit());

ipcMain.handle('load-config', () => loadConfig());
ipcMain.handle('save-config', (e, config) => saveConfig(config));

ipcMain.handle('copy-to-clipboard', (e, text) => {
  clipboard.writeText(text);
  return true;
});

ipcMain.handle('export-txt', async (e, text) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    title: '导出日报',
    defaultPath: `日报_${new Date().toISOString().slice(0,10)}.txt`,
    filters: [{ name: '文本文件', extensions: ['txt'] }]
  });
  if (!result.canceled && result.filePath) {
    fs.writeFileSync(result.filePath, text, 'utf-8');
    return { success: true, path: result.filePath };
  }
  return { success: false };
});
