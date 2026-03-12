package ui

import (
	"daily-report-generator/internal/config"
	"daily-report-generator/internal/modules"
	"daily-report-generator/internal/storage"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
	"time"
)

type MainWindow struct {
	window       fyne.Window
	cfg          *config.Config
	store        *storage.ConfigStore
	lastFocus    string // "today" or "next"
	
	// UI 组件
	unitNameEntry    *widget.Entry
	dateEntry        *widget.Entry
	regionEntry      *widget.Entry
	wellNameEntry    *widget.Entry
	designDepthEntry *widget.Entry
	currentDepthEntry *widget.Entry
	todayWorkEntry   *widget.Entry
	nextWorkEntry    *widget.Entry
	commStatusEntry  *widget.Entry
	managerPhoneEntry *widget.Entry
	thurayaPhoneEntry *widget.Entry
	securityStatusEntry *widget.Entry
}

func NewMainWindow(app fyne.App, cfg *config.Config, store *storage.ConfigStore) *MainWindow {
	mw := &MainWindow{
		window: app.NewWindow("🛢 每日报表生成器"),
		cfg:    cfg,
		store:  store,
	}
	
	mw.window.Resize(fyne.NewSize(1280, 800))
	mw.createUI()
	mw.loadConfig()
	
	return mw
}

func (mw *MainWindow) createUI() {
	// 菜单栏
	mainMenu := mw.createMenu()
	mw.window.SetMainMenu(mainMenu)
	
	// 基础信息区
	basicInfo := mw.createBasicInfo()
	
	// 工况编辑区
	opSection := mw.createOperationSection()
	
	// 人员通讯区
	staffSection := mw.createStaffSection()
	
	// 按钮区
	buttons := mw.createButtons()
	
	// 布局
	content := container.NewVBox(
		basicInfo,
		container.NewHSplit(opSection, staffSection),
		buttons,
	)
	
	mw.window.SetContent(content)
}

func (mw *MainWindow) createMenu() *fyne.MainMenu {
	newItem := widget.NewMenuItem("新建", func() { mw.newReport() })
	exportItem := widget.NewMenuItem("导出 TXT", func() { mw.exportTXT() })
	fileMenu := fyne.NewMenu("文件", newItem, exportItem)
	
	wizardItem := widget.NewMenuItem("重新运行向导", func() { mw.showWizard() })
	configMenu := fyne.NewMenu("配置", wizardItem)
	
	copyItem := widget.NewMenuItem("复制到剪贴板", func() { mw.copyToClipboard() })
	previewItem := widget.NewMenuItem("预览", func() { mw.preview() })
	toolMenu := fyne.NewMenu("工具", copyItem, previewItem)
	
	helpItem := widget.NewMenuItem("使用说明", func() { mw.showHelp() })
	aboutItem := widget.NewMenuItem("关于", func() { mw.showAbout() })
	helpMenu := fyne.NewMenu("帮助", helpItem, aboutItem)
	
	return fyne.NewMainMenu(fileMenu, configMenu, toolMenu, helpMenu)
}

func (mw *MainWindow) createBasicInfo() *widget.Card {
	mw.unitNameEntry = widget.NewEntry()
	mw.dateEntry = widget.NewEntry()
	mw.dateEntry.SetText(time.Now().Format("2006.01.02"))
	mw.regionEntry = widget.NewEntry()
	mw.wellNameEntry = widget.NewEntry()
	mw.designDepthEntry = widget.NewEntry()
	mw.currentDepthEntry = widget.NewEntry()
	
	form := widget.NewForm(
		widget.NewFormItem("单位名称", mw.unitNameEntry),
		widget.NewFormItem("日期", mw.dateEntry),
		widget.NewFormItem("区域", mw.regionEntry),
		widget.NewFormItem("井号", mw.wellNameEntry),
		widget.NewFormItem("设计井深", mw.designDepthEntry),
		widget.NewFormItem("当前井深", mw.currentDepthEntry),
	)
	
	return widget.NewCard("📋 基础信息", "", form)
}

func (mw *MainWindow) createOperationSection() *widget.Card {
	mw.todayWorkEntry = widget.NewEntry()
	mw.todayWorkEntry.SetPlaceHolder("点击词条添加到今日工况")
	mw.todayWorkEntry.OnFocusGained = func() { mw.lastFocus = "today" }
	
	mw.nextWorkEntry = widget.NewEntry()
	mw.nextWorkEntry.SetPlaceHolder("点击词条添加到下步工况")
	mw.nextWorkEntry.OnFocusGained = func() { mw.lastFocus = "next" }
	
	// 工况词条
	tokens := mw.createTokenButtons()
	
	content := container.NewVBox(
		widget.NewLabel("今日工况:"),
		mw.todayWorkEntry,
		widget.NewLabel("下步工况:"),
		mw.nextWorkEntry,
		widget.NewSeparator(),
		widget.NewLabel("🏷 工况词条（点击添加到当前焦点）:"),
		tokens,
	)
	
	return widget.NewCard("📝 工况编辑", "", content)
}

func (mw *MainWindow) createTokenButtons() *fyne.Container {
	tokens := mw.cfg.OperationTokens
	buttons := make([]fyne.CanvasObject, 0, len(tokens))
	
	for _, token := range tokens {
		if !token.Enabled {
			continue
		}
		btn := widget.NewButton(token.Text, func(t string) {
			mw.addToken(t)
		}(token.Text))
		buttons = append(buttons, btn)
	}
	
	return container.NewVBox(buttons...)
}

func (mw *MainWindow) createStaffSection() *widget.Card {
	mw.commStatusEntry = widget.NewEntry()
	mw.managerPhoneEntry = widget.NewEntry()
	mw.thurayaPhoneEntry = widget.NewEntry()
	mw.securityStatusEntry = widget.NewEntry()
	
	form := widget.NewForm(
		widget.NewFormItem("通讯情况", mw.commStatusEntry),
		widget.NewFormItem("平台经理电话", mw.managerPhoneEntry),
		widget.NewFormItem("Thuraya 电话", mw.thurayaPhoneEntry),
		widget.NewFormItem("安全情况", mw.securityStatusEntry),
	)
	
	return widget.NewCard("👥 人员与通讯", "", form)
}

func (mw *MainWindow) createButtons() *fyne.Container {
	generateBtn := widget.NewButton("📋 生成报表", func() { mw.generate() })
	copyBtn := widget.NewButton("📋 复制到剪贴板", func() { mw.copyToClipboard() })
	previewBtn := widget.NewButton("👁 预览", func() { mw.preview() })
	
	return container.NewHBox(generateBtn, copyBtn, previewBtn)
}

func (mw *MainWindow) loadConfig() {
	basic := mw.cfg.BasicInfo
	mw.unitNameEntry.SetText(basic.UnitName)
	mw.regionEntry.SetText(basic.Region)
	mw.wellNameEntry.SetText(basic.WellName)
	mw.designDepthEntry.SetText(string(rune(basic.DesignDepthValue)))
	
	contact := mw.cfg.ContactInfo
	mw.commStatusEntry.SetText(contact.CommunicationStatus)
	mw.managerPhoneEntry.SetText(contact.ManagerPhone)
	mw.thurayaPhoneEntry.SetText(contact.ThurayaPhone)
	mw.securityStatusEntry.SetText(contact.SecurityStatus)
}

func (mw *MainWindow) addToken(text string) {
	if mw.lastFocus == "today" {
		current := mw.todayWorkEntry.Text
		if current != "" && current[len(current)-1] != ',' {
			current += ","
		}
		mw.todayWorkEntry.SetText(current + text)
	} else {
		current := mw.nextWorkEntry.Text
		if current != "" && current[len(current)-1] != ',' {
			current += ","
		}
		mw.nextWorkEntry.SetText(current + text)
	}
}

func (mw *MainWindow) collectData() modules.ReportData {
	chineseTotal, bracketDetail, localName, localCount, otherForeign, specialNotes := 
		modules.CalculatePersonnel(mw.cfg.PersonnelItems)
	
	return modules.ReportData{
		UnitName:       mw.unitNameEntry.Text,
		ReportDate:     mw.dateEntry.Text,
		Region:         mw.regionEntry.Text,
		ChineseTotal:   chineseTotal,
		BracketDetail:  bracketDetail,
		LocalName:      localName,
		LocalCount:     localCount,
		OtherForeign:   otherForeign,
		SpecialNotes:   specialNotes,
		SupplyDays:     mw.cfg.BasicInfo.SupplyDays,
		DieselVolume:   mw.cfg.BasicInfo.DieselVolume,
		DieselDays:     mw.cfg.BasicInfo.DieselDays,
		WellName:       mw.wellNameEntry.Text,
		DesignDepth:    mw.cfg.BasicInfo.DesignDepthValue,
		DesignDepthUnit: mw.cfg.BasicInfo.DesignDepthUnit,
		TodayWork:      mw.todayWorkEntry.Text,
		CurrentDepth:   0, // TODO: parse from entry
		NextWork:       mw.nextWorkEntry.Text,
		CommStatus:     mw.commStatusEntry.Text,
		ManagerPhone:   mw.managerPhoneEntry.Text,
		ThurayaPhone:   mw.thurayaPhoneEntry.Text,
		SatInternal:    mw.cfg.ContactInfo.SatPhoneInternal,
		SatExternal:    mw.cfg.ContactInfo.SatPhoneExternal,
		SecurityStatus: mw.securityStatusEntry.Text,
	}
}

func (mw *MainWindow) generate() {
	data := mw.collectData()
	reportText := modules.GenerateReport(data)
	
	// 显示预览窗口
	preview := widget.NewLabel(reportText)
	preview.Wrapping = fyne.TextWrapWord
	
	previewWindow := mw.window.Fyne().NewWindow("📄 报表预览")
	previewWindow.SetContent(container.NewPadded(preview))
	previewWindow.Resize(fyne.NewSize(600, 400))
	previewWindow.Show()
}

func (mw *MainWindow) copyToClipboard() {
	data := mw.collectData()
	reportText := modules.GenerateReport(data)
	
	mw.window.Clipboard().SetContent(reportText)
	dialog.ShowInformation("成功", "报表已复制到剪贴板", mw.window)
}

func (mw *MainWindow) preview() {
	mw.generate()
}

func (mw *MainWindow) newReport() {
	mw.todayWorkEntry.SetText("")
	mw.nextWorkEntry.SetText("")
	mw.currentDepthEntry.SetText("")
}

func (mw *MainWindow) exportTXT() {
	dialog.ShowFileSave(func(writer fyne.URIWriteCloser, err error) {
		if err != nil || writer == nil {
			return
		}
		data := mw.collectData()
		reportText := modules.GenerateReport(data)
		writer.Write([]byte(reportText))
		writer.Close()
	}, mw.window)
}

func (mw *MainWindow) showWizard() {
	wizard := NewWizardWindow(mw.window.Fyne(), mw.cfg, mw.store)
	wizard.window.Show()
}

func (mw *MainWindow) showHelp() {
	helpText := `每日报表生成器 使用说明

1. 填写基础信息（单位、日期、井号等）
2. 点击工况词条自动添加到当前焦点输入框
3. 点击"生成报表"预览
4. 点击"复制到剪贴板"复制

焦点规则:
- 点击今日工况框，词条添加到今日工况
- 点击下步工况框，词条添加到下步工况

配置保存在:
%APPDATA%\DailyReportApp\config.json`

	dialog.ShowInformation("使用说明", helpText, mw.window)
}

func (mw *MainWindow) showAbout() {
	aboutText := `🛢 每日报表生成器
版本：v6.0.0 (Go 语言版)

By Freely QQ:20721
Pzxsky@Gmail.com

© 2026 All Rights Reserved.`

	dialog.ShowInformation("关于", aboutText, mw.window)
}

func (mw *MainWindow) ShowAndRun() {
	mw.window.ShowAndRun()
}
