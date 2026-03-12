package config

import (
	"encoding/json"
	"os"
	"path/filepath"
)

// Config 主配置结构
type Config struct {
	ConfigVersion   int              `json:"config_version"`
	BasicInfo       BasicInfo        `json:"basic_info"`
	PersonnelItems  []PersonnelItem  `json:"personnel_items"`
	ContactInfo     ContactInfo      `json:"contact_info"`
	OperationTokens []OperationToken `json:"operation_tokens"`
}

// BasicInfo 基础信息
type BasicInfo struct {
	UnitName         string `json:"unit_name"`
	Region           string `json:"region"`
	WellName         string `json:"well_name"`
	DesignDepthValue int    `json:"design_depth_value"`
	DesignDepthUnit  string `json:"design_depth_unit"`
	SupplyDays       int    `json:"supply_days"`
	DieselVolume     int    `json:"diesel_volume"`
	DieselDays       int    `json:"diesel_days"`
}

// PersonnelItem 人员项
type PersonnelItem struct {
	ID                    string `json:"id"`
	Name                  string `json:"name"`
	CategoryTag           string `json:"category_tag"`
	Count                 int    `json:"count"`
	IncludeInBracket      bool   `json:"include_in_bracket"`
	IncludeInChineseTotal bool   `json:"include_in_chinese_total"`
	IncludeInLocalTotal   bool   `json:"include_in_local_total"`
	SpecialTitle          string `json:"special_title"`
	SpecialName           string `json:"special_name"`
	SpecialAction         string `json:"special_action"`
	SortOrder             int    `json:"sort_order"`
	Enabled               bool   `json:"enabled"`
}

// ContactInfo 通讯信息
type ContactInfo struct {
	CommunicationStatus string `json:"communication_status"`
	ManagerPhone        string `json:"manager_phone"`
	ThurayaPhone        string `json:"thuraya_phone"`
	SatPhoneInternal    string `json:"sat_phone_internal"`
	SatPhoneExternal    string `json:"sat_phone_external"`
	SecurityStatus      string `json:"security_status"`
}

// OperationToken 工况词条
type OperationToken struct {
	ID        string `json:"id"`
	Text      string `json:"text"`
	SortOrder int    `json:"sort_order"`
	Enabled   bool   `json:"enabled"`
}

// LoadConfig 加载配置
func LoadConfig() (*Config, error) {
	configPath := getConfigPath()
	
	data, err := os.ReadFile(configPath)
	if err != nil {
		return DefaultConfig(), nil
	}
	
	var cfg Config
	err = json.Unmarshal(data, &cfg)
	if err != nil {
		return DefaultConfig(), nil
	}
	
	return &cfg, nil
}

// SaveConfig 保存配置
func SaveConfig(cfg *Config) error {
	configPath := getConfigPath()
	
	dir := filepath.Dir(configPath)
	os.MkdirAll(dir, 0755)
	
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}
	
	return os.WriteFile(configPath, data, 0644)
}

// DefaultConfig 默认配置
func DefaultConfig() *Config {
	return &Config{
		ConfigVersion: 1,
		BasicInfo: BasicInfo{
			UnitName:         "Rig919",
			Region:           "H",
			WellName:         "",
			DesignDepthValue: 1000,
			DesignDepthUnit:  "m",
			SupplyDays:       30,
			DieselVolume:     50,
			DieselDays:       15,
		},
		PersonnelItems: getDefaultPersonnel(),
		ContactInfo:    getDefaultContact(),
		OperationTokens: getDefaultTokens(),
	}
}

func getDefaultPersonnel() []PersonnelItem {
	return []PersonnelItem{
		{ID: "unit_chinese", Name: "919 队", CategoryTag: "chinese", Count: 14,
			IncludeInBracket: true, IncludeInChineseTotal: true, SortOrder: 10, Enabled: true},
		{ID: "cook", Name: "外聘厨师", CategoryTag: "chinese", Count: 3,
			IncludeInBracket: true, IncludeInChineseTotal: true, SortOrder: 20, Enabled: true},
		{ID: "local", Name: "919 队当地雇员", CategoryTag: "local", Count: 29,
			IncludeInLocalTotal: true, SortOrder: 10, Enabled: true},
		{ID: "soldier", Name: "士兵", CategoryTag: "local", Count: 8,
			IncludeInLocalTotal: true, SortOrder: 20, Enabled: true},
		{ID: "manager", Name: "基地经理", CategoryTag: "special", Count: 1,
			IncludeInBracket: true, IncludeInChineseTotal: true, SortOrder: 100, Enabled: true,
			SpecialTitle: "基地经理", SpecialName: "赵铁寨", SpecialAction: "驻井指导工作"},
	}
}

func getDefaultContact() ContactInfo {
	return ContactInfo{
		CommunicationStatus: "当地手机信号差",
		ManagerPhone:        "00235-93577318",
		ThurayaPhone:        "008821621906786",
		SatPhoneInternal:    "6660353（内线）",
		SatPhoneExternal:    "021-80246760（外线）",
		SecurityStatus:      "周边安全无异常",
	}
}

func getDefaultTokens() []OperationToken {
	return []OperationToken{
		{ID: "t1", Text: "下套管", SortOrder: 10, Enabled: true},
		{ID: "t2", Text: "循环", SortOrder: 20, Enabled: true},
		{ID: "t3", Text: "固井", SortOrder: 30, Enabled: true},
		{ID: "t4", Text: "候凝", SortOrder: 40, Enabled: true},
		{ID: "t5", Text: "安装套管头", SortOrder: 50, Enabled: true},
		{ID: "t6", Text: "安装 BOP", SortOrder: 60, Enabled: true},
		{ID: "t7", Text: "试压", SortOrder: 70, Enabled: true},
		{ID: "t8", Text: "BOP 试压", SortOrder: 80, Enabled: true},
		{ID: "t9", Text: "组合二开钻具", SortOrder: 90, Enabled: true},
		{ID: "t10", Text: "下钻", SortOrder: 100, Enabled: true},
		{ID: "t11", Text: "钻塞", SortOrder: 110, Enabled: true},
		{ID: "t12", Text: "二开钻进", SortOrder: 120, Enabled: true},
	}
}

func getConfigPath() string {
	configDir := getConfigDir()
	return filepath.Join(configDir, "config.json")
}

func getConfigDir() string {
	// Windows: %APPDATA%\DailyReportApp
	appData := os.Getenv("APPDATA")
	if appData != "" {
		return filepath.Join(appData, "DailyReportApp")
	}
	
	// Fallback
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".daily-report")
}
