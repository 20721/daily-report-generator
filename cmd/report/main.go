package main

import (
	"daily-report-generator/internal/config"
	"daily-report-generator/internal/storage"
	"daily-report-generator/internal/ui"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/dialog"
	"log"
)

func main() {
	log.Println("每日报表生成器启动...")
	
	// 加载配置
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Printf("配置加载失败，使用默认配置：%v", err)
		cfg = config.DefaultConfig()
	}
	
	// 初始化存储
	store := storage.NewConfigStore()
	
	// 创建应用
	myApp := app.New()
	
	// 检查是否首次运行
	if cfg.UnitName == "" {
		// 显示向导
		wizard := ui.NewWizardWindow(myApp, cfg, store)
		wizard.ShowAndRun()
	} else {
		// 显示主窗口
		mainWindow := ui.NewMainWindow(myApp, cfg, store)
		mainWindow.ShowAndRun()
	}
}

func showStartupError(a app.App, err error) {
	dialog.ShowError(err, a.NewWindow("启动错误"))
}
