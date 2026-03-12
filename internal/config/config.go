package config

import (
	"encoding/json"
	"os"
	"path/filepath"
)

type Config struct {
	UnitName         string `json:"unit_name"`
	Region           string `json:"region"`
	WellName         string `json:"well_name"`
	DesignDepth      int    `json:"design_depth"`
	CurrentDepth     int    `json:"current_depth"`
	SupplyDays       int    `json:"supply_days"`
	DieselVolume     int    `json:"diesel_volume"`
	DieselDays       int    `json:"diesel_days"`
	TodayWork        string `json:"today_work"`
	NextWork         string `json:"next_work"`
	CommStatus       string `json:"comm_status"`
	ManagerPhone     string `json:"manager_phone"`
	ThurayaPhone     string `json:"thuraya_phone"`
	SecurityStatus   string `json:"security_status"`
	ChineseCount     int    `json:"chinese_count"`
	LocalCount       int    `json:"local_count"`
	SoldierCount     int    `json:"soldier_count"`
	ManagerName      string `json:"manager_name"`
}

func LoadConfig() (*Config, error) {
	path := getConfigPath()
	data, err := os.ReadFile(path)
	if err != nil {
		return DefaultConfig(), nil
	}
	
	var cfg Config
	json.Unmarshal(data, &cfg)
	return &cfg, nil
}

func SaveConfig(cfg *Config) error {
	path := getConfigPath()
	os.MkdirAll(filepath.Dir(path), 0755)
	data, _ := json.MarshalIndent(cfg, "", "  ")
	return os.WriteFile(path, data, 0644)
}

func DefaultConfig() *Config {
	return &Config{
		UnitName:       "Rig919",
		Region:         "H",
		SupplyDays:     30,
		DieselVolume:   50,
		DieselDays:     15,
		ChineseCount:   14,
		LocalCount:     29,
		SoldierCount:   8,
		ManagerName:    "赵铁寨",
		CommStatus:     "当地手机信号差",
		ManagerPhone:   "00235-93577318",
		ThurayaPhone:   "008821621906786",
		SecurityStatus: "周边安全无异常",
	}
}

func getConfigPath() string {
	appData := os.Getenv("APPDATA")
	if appData != "" {
		return filepath.Join(appData, "DailyReportApp", "config.json")
	}
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".daily-report", "config.json")
}
