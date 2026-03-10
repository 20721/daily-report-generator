const { ipcRenderer } = require('electron');

let config = {};
let selectedToday = new Set();
let selectedNext = new Set();

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
  document.getElementById('date').valueAsDate = new Date();
  config = await ipcRenderer.invoke('load-config');
  loadConfigToUI();
  renderStaffGrid();
  renderConditions();
});

function loadConfigToUI() {
  document.getElementById('unitName').value = config.unitName || 'Rig919';
  document.getElementById('area').value = config.area || 'H';
  document.getElementById('wellName').value = config.wellName || '';
  document.getElementById('designDepth').value = config.designDepth || '';
  document.getElementById('manager').value = config.manager || '';
  document.getElementById('phone').value = config.phone || '';
  document.getElementById('thuraya').value = config.thuraya || '';
  document.getElementById('satInternal').value = config.satInternal || '';
  document.getElementById('satExternal').value = config.satExternal || '';
}

function renderStaffGrid() {
  const grid = document.getElementById('staffGrid');
  const groups = config.staffGroups || {};
  grid.innerHTML = Object.entries(groups).map(([name, count]) => `
    <div class="staff-item">
      <label>${name}</label>
      <input type="number" data-group="${name}" value="${count}" min="0">
    </div>
  `).join('');
}

function renderConditions() {
  const workCond = config.workConditions || [];
  const todayDiv = document.getElementById('todayConditions');
  todayDiv.innerHTML = workCond.map(c => `
    <span class="condition-tag" onclick="toggleCondition(this, 'today')">${c}</span>
  `).join('');
}

function toggleCondition(el, type) {
  el.classList.toggle('selected');
  const text = el.textContent.trim();
  if (type === 'today') {
    el.classList.contains('selected') ? selectedToday.add(text) : selectedToday.delete(text);
  } else {
    el.classList.contains('selected') ? selectedNext.add(text) : selectedNext.delete(text);
  }
}

function addCustomCondition(type) {
  const input = document.getElementById(type === 'today' ? 'customTodayCondition' : 'customNextCondition');
  const text = input.value.trim();
  if (!text) return;
  
  const div = document.createElement('span');
  div.className = 'condition-tag selected';
  div.innerHTML = `${text}<span class="remove" onclick="removeCustom(this, '${type}')">×</span>`;
  div.onclick = (e) => { if (e.target !== e.currentTarget.querySelector('.remove')) toggleCondition(div, type); };
  
  const container = document.getElementById(type === 'today' ? 'todayConditions' : 'nextConditions');
  container.appendChild(div);
  input.value = '';
  
  if (type === 'today') selectedToday.add(text);
  else selectedNext.add(text);
}

function removeCustom(el, type) {
  el.parentElement.remove();
  const text = el.parentElement.textContent.replace('×', '').trim();
  if (type === 'today') selectedToday.delete(text);
  else selectedNext.delete(text);
}

function generateReport() {
  const data = {
    unitName: document.getElementById('unitName').value,
    date: document.getElementById('date').value,
    area: document.getElementById('area').value,
    wellName: document.getElementById('wellName').value,
    designDepth: document.getElementById('designDepth').value,
    currentDepth: document.getElementById('currentDepth').value,
    foodDays: document.getElementById('foodDays').value,
    dieselAmount: document.getElementById('dieselAmount').value,
    dieselDays: document.getElementById('dieselDays').value,
    manager: document.getElementById('manager').value,
    managerOnSite: document.getElementById('managerOnSite').checked,
    phone: document.getElementById('phone').value,
    thuraya: document.getElementById('thuraya').value,
    satInternal: document.getElementById('satInternal').value,
    satExternal: document.getElementById('satExternal').value,
    safety: document.getElementById('safety').value
  };

  // 人员统计
  const staffInputs = document.querySelectorAll('#staffGrid input');
  const staffSummary = [];
  let totalChinese = 0;
  staffInputs.forEach(input => {
    const count = parseInt(input.value) || 0;
    const group = input.dataset.group;
    if (count > 0) {
      staffSummary.push(`${group}${count}人`);
      if (!['当地雇员', '士兵', '安保'].includes(group)) totalChinese += count;
    }
  });

  const todayList = Array.from(selectedToday);
  const nextList = Array.from(selectedNext);

  let report = `1.单位名称：${data.unitName}\n`;
  report += `2.日期：${data.date}\n`;
  report += `3.所在区域：${data.area}\n`;
  report += `4.人员情况：中方人员${totalChinese}人（${staffSummary.filter(s => !s.includes('当地雇员') && !s.includes('士兵') && !s.includes('安保')).join('，')}）${staffSummary.find(s => s.includes('当地雇员')) || '当地雇员 0 人'}；${staffSummary.find(s => s.includes('士兵')) || '士兵 0 人'}，${staffSummary.find(s => s.includes('安保')) || '安保 0 人'}，${data.managerOnSite ? `基地经理${data.manager}驻井指导工作` : ''}。\n`;
  report += `5.生活物资储备天数：${data.foodDays}天；井场柴油${data.dieselAmount}方，可用${data.dieselDays}天。\n`;
  report += `6.井号：${data.wellName} 设计井深：${data.designDepth} m\n`;
  report += `7.今日工况：${todayList.join('，') || '无'}。\n`;
  report += `8.当前井深：${data.currentDepth || ''}米\n`;
  report += `9.下步工况：${nextList.join('，') || '无'}。\n`;
  report += `10.通讯情况：当地手机信号差，平台经理：${data.phone}\n`;
  report += `Thuraya 电话：${data.thuraya}卫星网络座机：${data.satInternal}（内线）${data.satExternal}（外线）\n`;
  report += `11.安全情况：${data.safety}`;

  document.getElementById('preview').value = report;
  window.lastReport = report;
  return report;
}

async function copyReport() {
  const report = window.lastReport || generateReport();
  await ipcRenderer.invoke('copy-to-clipboard', report);
  alert('✅ 已复制到剪贴板');
}

async function exportTxt() {
  const report = window.lastReport || generateReport();
  const result = await ipcRenderer.invoke('export-txt', report);
  if (result.success) alert(`✅ 已导出到：${result.path}`);
}

async function saveConfig() {
  config.unitName = document.getElementById('unitName').value;
  config.area = document.getElementById('area').value;
  config.wellName = document.getElementById('wellName').value;
  config.designDepth = document.getElementById('designDepth').value;
  config.manager = document.getElementById('manager').value;
  config.phone = document.getElementById('phone').value;
  config.thuraya = document.getElementById('thuraya').value;
  config.satInternal = document.getElementById('satInternal').value;
  config.satExternal = document.getElementById('satExternal').value;

  const staffInputs = document.querySelectorAll('#staffGrid input');
  staffInputs.forEach(input => {
    config.staffGroups[input.dataset.group] = parseInt(input.value) || 0;
  });

  const success = await ipcRenderer.invoke('save-config', config);
  alert(success ? '✅ 配置已保存' : '❌ 保存失败');
}
