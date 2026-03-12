package modules

import (
	"daily-report-generator/internal/config"
	"fmt"
	"strings"
)

// ReportData 报表数据
type ReportData struct {
	UnitName         string
	ReportDate       string
	Region           string
	ChineseTotal     int
	BracketDetail    []string
	LocalName        string
	LocalCount       int
	OtherForeign     []string
	SpecialNotes     []string
	SupplyDays       int
	DieselVolume     int
	DieselDays       int
	WellName         string
	DesignDepth      int
	DesignDepthUnit  string
	TodayWork        string
	CurrentDepth     int
	NextWork         string
	CommStatus       string
	ManagerPhone     string
	ThurayaPhone     string
	SatInternal      string
	SatExternal      string
	SecurityStatus   string
}

// GenerateReport 生成报表
func GenerateReport(data ReportData) string {
	var sb strings.Builder
	
	sb.WriteString(fmt.Sprintf("1.单位名称：%s\n", data.UnitName))
	sb.WriteString(fmt.Sprintf("2.日期：%s\n", data.ReportDate))
	sb.WriteString(fmt.Sprintf("3.所在区域：%s\n", data.Region))
	
	// 人员情况
	sb.WriteString("4.人员情况：")
	sb.WriteString(fmt.Sprintf("中方人员%d人", data.ChineseTotal))
	
	if len(data.BracketDetail) > 0 {
		sb.WriteString("（其中" + strings.Join(data.BracketDetail, "，") + "）")
	}
	
	if data.LocalName != "" && data.LocalCount > 0 {
		sb.WriteString(fmt.Sprintf("%s 当地雇员%d人", data.LocalName, data.LocalCount))
	}
	
	if len(data.OtherForeign) > 0 {
		sb.WriteString("；" + strings.Join(data.OtherForeign, "，"))
	}
	
	if len(data.SpecialNotes) > 0 {
		sb.WriteString("，" + strings.Join(data.SpecialNotes, "，"))
	}
	sb.WriteString("\n")
	
	sb.WriteString(fmt.Sprintf("5.生活物资储备天数：%d天；井场柴油%d方，可用%d天。\n", 
		data.SupplyDays, data.DieselVolume, data.DieselDays))
	sb.WriteString(fmt.Sprintf("6.井号：%s 设计井深：%d %s\n", 
		data.WellName, data.DesignDepth, data.DesignDepthUnit))
	sb.WriteString(fmt.Sprintf("7.今日工况：%s。\n", data.TodayWork))
	sb.WriteString(fmt.Sprintf("8.当前井深：%dm\n", data.CurrentDepth))
	sb.WriteString(fmt.Sprintf("9.下步工况：%s。\n", data.NextWork))
	
	sb.WriteString("10.通讯情况：")
	parts := []string{
		data.CommStatus,
		"平台经理：" + data.ManagerPhone,
		"Thuraya 电话：" + data.ThurayaPhone,
		"卫星网络座机：" + data.SatInternal + " " + data.SatExternal,
		"安全情况：" + data.SecurityStatus,
	}
	sb.WriteString(strings.Join(parts, "，"))
	
	return sb.String()
}

// CalculatePersonnel 计算人员统计
func CalculatePersonnel(items []config.PersonnelItem) (chineseTotal int, bracketDetail []string, 
	localName string, localCount int, otherForeign []string, specialNotes []string) {
	
	for _, item := range items {
		if !item.Enabled {
			continue
		}
		
		if item.IncludeInChineseTotal {
			chineseTotal += item.Count
		}
		
		if item.IncludeInBracket && item.IncludeInChineseTotal {
			bracketDetail = append(bracketDetail, fmt.Sprintf("%s%d人", item.Name, item.Count))
		}
		
		if item.CategoryTag == "local" && strings.Contains(item.Name, "当地雇员") {
			localName = strings.Replace(item.Name, "当地雇员", "", 1)
			localCount = item.Count
		}
		
		if item.CategoryTag == "local" && !strings.Contains(item.Name, "当地雇员") {
			otherForeign = append(otherForeign, fmt.Sprintf("%s%d人", item.Name, item.Count))
		}
		
		if item.CategoryTag == "special" && item.SpecialName != "" {
			specialNotes = append(specialNotes, 
				fmt.Sprintf("%s%s%s", item.SpecialTitle, item.SpecialName, item.SpecialAction))
		}
	}
	
	return
}
