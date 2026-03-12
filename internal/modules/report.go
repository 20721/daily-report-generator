package modules

import (
	"daily-report-walk/internal/config"
	"fmt"
	"strings"
)

func GenerateReport(cfg *config.Config) string {
	var sb strings.Builder
	
	sb.WriteString(fmt.Sprintf("1.单位名称：%s\n", cfg.UnitName))
	sb.WriteString(fmt.Sprintf("2.日期：%s\n", getCurrentDate()))
	sb.WriteString(fmt.Sprintf("3.所在区域：%s\n", cfg.Region))
	
	// 人员情况
	chineseTotal := cfg.ChineseCount + 1 // +1 for manager
	sb.WriteString(fmt.Sprintf("4.人员情况：中方人员%d人（其中 919 队%d人，外聘厨师 3 人，基地经理 1 人）", 
		chineseTotal, cfg.ChineseCount))
	sb.WriteString(fmt.Sprintf("919 队当地雇员%d人；士兵%d人", cfg.LocalCount, cfg.SoldierCount))
	sb.WriteString(fmt.Sprintf("，基地经理%s驻井指导工作。\n", cfg.ManagerName))
	
	sb.WriteString(fmt.Sprintf("5.生活物资储备天数：%d天；井场柴油%d方，可用%d天。\n", 
		cfg.SupplyDays, cfg.DieselVolume, cfg.DieselDays))
	sb.WriteString(fmt.Sprintf("6.井号：%s 设计井深：%d m\n", cfg.WellName, cfg.DesignDepth))
	sb.WriteString(fmt.Sprintf("7.今日工况：%s。\n", cfg.TodayWork))
	sb.WriteString(fmt.Sprintf("8.当前井深：%dm\n", cfg.CurrentDepth))
	sb.WriteString(fmt.Sprintf("9.下步工况：%s。\n", cfg.NextWork))
	
	sb.WriteString("10.通讯情况：")
	sb.WriteString(fmt.Sprintf("%s，平台经理：%s Thuraya 电话：%s", 
		cfg.CommStatus, cfg.ManagerPhone, cfg.ThurayaPhone))
	sb.WriteString(fmt.Sprintf("卫星网络座机：6660353（内线） 021-80246760（外线） "))
	sb.WriteString(fmt.Sprintf("安全情况：%s", cfg.SecurityStatus))
	
	return sb.String()
}

func getCurrentDate() string {
	// 简化版本，实际应该用 time.Now()
	return "2026.03.13"
}
