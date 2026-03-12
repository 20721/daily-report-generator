package main

import (
	"daily-report-walk/internal/config"
	"daily-report-walk/internal/ui"
	"github.com/lxn/walk"
	. "github.com/lxn/walk/declarative"
	"log"
)

func main() {
	log.Println("每日报表生成器 Walk 版启动...")
	
	// 加载配置
	cfg, err := config.LoadConfig()
	if err != nil {
		cfg = config.DefaultConfig()
	}
	
	// 创建主窗口
	mainWin, err := ui.NewMainWindow(cfg)
	if err != nil {
		log.Fatal(err)
	}
	
	mainWin.Run()
}
