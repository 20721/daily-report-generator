package main

import (
	"daily-report-walk/internal/config"
	"daily-report-walk/internal/ui"
	"github.com/lxn/walk"
	. "github.com/lxn/walk/declarative"
)

func main() {
	walk.InitMainWindow()
	
	// 加载配置
	cfg, _ := config.LoadConfig()
	
	// 创建主窗口
	mainWin, _ := ui.NewMainWindow(cfg)
	mainWin.Run()
}
