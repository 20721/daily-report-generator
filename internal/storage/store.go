package storage

import (
	"daily-report-walk/internal/config"
	"encoding/json"
	"os"
	"path/filepath"
	"time"
)

type ConfigStore struct{}

func NewConfigStore() *ConfigStore {
	return &ConfigStore{}
}

func (s *ConfigStore) Save(cfg *config.Config) error {
	return config.SaveConfig(cfg)
}

func (s *ConfigStore) Load() (*config.Config, error) {
	return config.LoadConfig()
}

func (s *ConfigStore) SaveReport(content string) error {
	dir := getConfigDir()
	os.MkdirAll(dir, 0755)
	
	filename := time.Now().Format("20060102_150405") + ".json"
	path := filepath.Join(dir, filename)
	
	data, _ := json.Marshal(map[string]string{
		"content":   content,
		"timestamp": time.Now().Format(time.RFC3339),
	})
	
	return os.WriteFile(path, data, 0644)
}

func getConfigDir() string {
	appData := os.Getenv("APPDATA")
	if appData != "" {
		return filepath.Join(appData, "DailyReportApp", "report_history")
	}
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".daily-report", "report_history")
}
