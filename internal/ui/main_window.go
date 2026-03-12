package ui

import (
	"daily-report-walk/internal/config"
	"daily-report-walk/internal/modules"
	"github.com/lxn/walk"
	. "github.com/lxn/walk/declarative"
	"time"
)

type MainWindow struct {
	*walk.MainWindow
	
	cfg *config.Config
	
	// UI 组件引用
	unitNameEdit     *walk.LineEdit
	dateEdit         *walk.LineEdit
	regionEdit       *walk.LineEdit
	wellNameEdit     *walk.LineEdit
	designDepthEdit  *walk.LineEdit
	currentDepthEdit *walk.LineEdit
	todayWorkEdit    *walk.TextEdit
	nextWorkEdit     *walk.TextEdit
	commStatusEdit   *walk.LineEdit
	managerPhoneEdit *walk.LineEdit
	thurayaPhoneEdit *walk.LineEdit
	securityEdit     *walk.LineEdit
	chineseCountEdit *walk.LineEdit
	localCountEdit   *walk.LineEdit
	soldierCountEdit *walk.LineEdit
	managerNameEdit  *walk.LineEdit
}

func NewMainWindow(cfg *config.Config) (*MainWindow, error) {
	mw := &MainWindow{cfg: cfg}
	
	err := walk.InitMainWindow()
	if err != nil {
		return nil, err
	}
	
	// 使用 declarative 方式创建窗口
	decl := MainWindowDecl{
		AssignTo: &mw.MainWindow,
		Title:    "🛢 每日报表生成器 (Go 版)",
		Size:     Size{Width: 1280, Height: 800},
		Layout:   VBox{},
		Children: []Widget{
			mw.createBasicInfo(),
			mw.createPersonnel(),
			mw.createWorkEdit(),
			mw.createContact(),
			mw.createButtons(),
		},
	}
	
	_, err = decl.Create()
	if err != nil {
		return nil, err
	}
	
	mw.loadConfig()
	
	return mw, nil
}

func (mw *MainWindow) createBasicInfo() Widget {
	return GroupBox{
		Title:  "📋 基础信息",
		Layout: Grid{Columns: 2},
		Children: []Widget{
			Label{Text: "单位名称:"},
			LineEdit{AssignTo: &mw.unitNameEdit},
			Label{Text: "日期:"},
			LineEdit{AssignTo: &mw.dateEdit, Text: time.Now().Format("2006.01.02")},
			Label{Text: "区域:"},
			LineEdit{AssignTo: &mw.regionEdit},
			Label{Text: "井号:"},
			LineEdit{AssignTo: &mw.wellNameEdit},
			Label{Text: "设计井深 (m):"},
			LineEdit{AssignTo: &mw.designDepthEdit},
			Label{Text: "当前井深 (m):"},
			LineEdit{AssignTo: &mw.currentDepthEdit},
		},
	}
}

func (mw *MainWindow) createPersonnel() Widget {
	return GroupBox{
		Title:  "👥 人员配置",
		Layout: Grid{Columns: 2},
		Children: []Widget{
			Label{Text: "中方人数:"},
			LineEdit{AssignTo: &mw.chineseCountEdit, Text: "14"},
			Label{Text: "当地雇员:"},
			LineEdit{AssignTo: &mw.localCountEdit, Text: "29"},
			Label{Text: "士兵:"},
			LineEdit{AssignTo: &mw.soldierCountEdit, Text: "8"},
			Label{Text: "基地经理:"},
			LineEdit{AssignTo: &mw.managerNameEdit, Text: "赵铁寨"},
		},
	}
}

func (mw *MainWindow) createWorkEdit() Widget {
	return GroupBox{
		Title:  "📝 工况编辑",
		Layout: VBox{},
		Children: []Widget{
			HBox{
				Children: []Widget{
					Label{Text: "今日工况:", MinWidth: 80},
					TextEdit{AssignTo: &mw.todayWorkEdit, MinHeight: 60},
				},
			},
			HBox{
				Children: []Widget{
					Label{Text: "下步工况:", MinWidth: 80},
					TextEdit{AssignTo: &mw.nextWorkEdit, MinHeight: 60},
				},
			},
		},
	}
}

func (mw *MainWindow) createContact() Widget {
	return GroupBox{
		Title:  "📞 通讯信息",
		Layout: Grid{Columns: 2},
		Children: []Widget{
			Label{Text: "通讯情况:"},
			LineEdit{AssignTo: &mw.commStatusEdit},
			Label{Text: "平台经理电话:"},
			LineEdit{AssignTo: &mw.managerPhoneEdit},
			Label{Text: "Thuraya 电话:"},
			LineEdit{AssignTo: &mw.thurayaPhoneEdit},
			Label{Text: "安全情况:"},
			LineEdit{AssignTo: &mw.securityEdit},
		},
	}
}

func (mw *MainWindow) createButtons() Widget {
	var generateBtn *walk.PushButton
	var copyBtn *walk.PushButton
	
	return HBox{
		Children: []Widget{
			PushButton{
				AssignTo: &generateBtn,
				Text:     "📋 生成报表",
				OnClicked: func() { mw.generate() },
			},
			PushButton{
				AssignTo: &copyBtn,
				Text:     "📋 复制到剪贴板",
				OnClicked: func() { mw.copyToClipboard() },
			},
			PushButton{
				Text:      "👁 预览",
				OnClicked: func() { mw.preview() },
			},
		},
	}
}

func (mw *MainWindow) loadConfig() {
	mw.unitNameEdit.SetText(mw.cfg.UnitName)
	mw.regionEdit.SetText(mw.cfg.Region)
	mw.wellNameEdit.SetText(mw.cfg.WellName)
	mw.commStatusEdit.SetText(mw.cfg.CommStatus)
	mw.managerPhoneEdit.SetText(mw.cfg.ManagerPhone)
	mw.thurayaPhoneEdit.SetText(mw.cfg.ThurayaPhone)
	mw.securityEdit.SetText(mw.cfg.SecurityStatus)
}

func (mw *MainWindow) collectData() *config.Config {
	return mw.cfg
}

func (mw *MainWindow) generate() {
	reportText := modules.GenerateReport(mw.cfg)
	walk.MsgBox(mw.MainWindow, "📄 报表预览", reportText, walk.MsgBoxOK)
}

func (mw *MainWindow) copyToClipboard() {
	reportText := modules.GenerateReport(mw.cfg)
	walk.Clipboard().SetText(reportText)
	walk.MsgBox(mw.MainWindow, "成功", "报表已复制到剪贴板", walk.MsgBoxOK)
}

func (mw *MainWindow) preview() {
	mw.generate()
}

func (mw *MainWindow) Run() {
	mw.MainWindow.Run()
}
