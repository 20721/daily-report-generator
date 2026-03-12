package ui

import (
	"daily-report-generator/internal/config"
	"daily-report-generator/internal/storage"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
)

type WizardWindow struct {
	window      fyne.Window
	cfg         *config.Config
	store       *storage.ConfigStore
	currentPage int
}

func NewWizardWindow(app fyne.App, cfg *config.Config, store *storage.ConfigStore) *WizardWindow {
	ww := &WizardWindow{
		window: app.NewWindow("🎉 欢迎使用每日报表生成器 - 首次配置向导"),
		cfg:    cfg,
		store:  store,
	}
	
	ww.window.Resize(fyne.NewSize(700, 550))
	ww.createUI()
	
	return ww
}

func (ww *WizardWindow) createUI() {
	// 进度标签
	progressLabel := widget.NewLabel("第 1 页 / 共 3 页")
	
	// 页面内容
	pageFrame := container.NewStack()
	
	// 按钮
	prevBtn := widget.NewButton("上一步", func() {})
	prevBtn.Disable()
	
	nextBtn := widget.NewButton("下一步", func() {})
	
	// 创建页面
	pages := ww.createPages()
	pageFrame.Add(pages[0])
	
	nextBtn.OnTapped = func() {
		if ww.currentPage < len(pages)-1 {
			ww.currentPage++
			pageFrame.Add(pages[ww.currentPage])
			progressLabel.SetText(string(rune('第' + ww.currentPage + 1) + "页 / 共 3 页"))
			if ww.currentPage == len(pages)-1 {
				nextBtn.SetText("完成")
			}
		} else {
			ww.finish()
		}
	}
	
	content := container.NewBorder(
		progressLabel,
		container.NewHBox(prevBtn, nextBtn),
		nil, nil,
		pageFrame,
	)
	
	ww.window.SetContent(container.NewPadded(content))
}

func (ww *WizardWindow) createPages() []fyne.CanvasObject {
	// 第 1 页：基础信息
	page1 := ww.createBasicInfoPage()
	
	// 第 2 页：人员配置
	page2 := ww.createPersonnelPage()
	
	// 第 3 页：通讯信息
	page3 := ww.createContactPage()
	
	return []fyne.CanvasObject{page1, page2, page3}
}

func (ww *WizardWindow) createBasicInfoPage() fyne.CanvasObject {
	unitNameEntry := widget.NewEntry()
	unitNameEntry.SetText(ww.cfg.BasicInfo.UnitName)
	
	regionEntry := widget.NewEntry()
	regionEntry.SetText(ww.cfg.BasicInfo.Region)
	
	wellNameEntry := widget.NewEntry()
	wellNameEntry.SetText(ww.cfg.BasicInfo.WellName)
	
	designDepthEntry := widget.NewEntry()
	designDepthEntry.SetText(string(rune(ww.cfg.BasicInfo.DesignDepthValue)))
	
	form := widget.NewForm(
		widget.NewFormItem("单位名称", unitNameEntry),
		widget.NewFormItem("所在区域", regionEntry),
		widget.NewFormItem("井号", wellNameEntry),
		widget.NewFormItem("设计井深 (m)", designDepthEntry),
	)
	
	return container.NewVBox(
		widget.NewLabelWithStyle("📋 基础信息", fyne.TextAlignLeading, fyne.TextStyle{Bold: true}),
		form,
	)
}

func (ww *WizardWindow) createPersonnelPage() fyne.CanvasObject {
	return widget.NewLabel("人员配置页面（简化版，使用默认值）")
}

func (ww *WizardWindow) createContactPage() fyne.CanvasObject {
	managerPhoneEntry := widget.NewEntry()
	managerPhoneEntry.SetText(ww.cfg.ContactInfo.ManagerPhone)
	
	thurayaPhoneEntry := widget.NewEntry()
	thurayaPhoneEntry.SetText(ww.cfg.ContactInfo.ThurayaPhone)
	
	commStatusEntry := widget.NewEntry()
	commStatusEntry.SetText(ww.cfg.ContactInfo.CommunicationStatus)
	
	securityStatusEntry := widget.NewEntry()
	securityStatusEntry.SetText(ww.cfg.ContactInfo.SecurityStatus)
	
	form := widget.NewForm(
		widget.NewFormItem("平台经理电话", managerPhoneEntry),
		widget.NewFormItem("Thuraya 电话", thurayaPhoneEntry),
		widget.NewFormItem("通讯情况", commStatusEntry),
		widget.NewFormItem("安全情况", securityStatusEntry),
	)
	
	return container.NewVBox(
		widget.NewLabelWithStyle("📞 通讯信息", fyne.TextAlignLeading, fyne.TextStyle{Bold: true}),
		form,
	)
}

func (ww *WizardWindow) finish() {
	err := ww.store.Save(ww.cfg)
	if err != nil {
		dialog.ShowError(err, ww.window)
		return
	}
	
	dialog.ShowInformation("完成", "配置已保存！\n\n现在可以开始使用每日报表生成器了。", ww.window)
	ww.window.Close()
}

func (ww *WizardWindow) Show() {
	ww.window.Show()
}
