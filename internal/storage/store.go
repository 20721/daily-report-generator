package storage

import (
	"daily-report-generator/internal/config"
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

// SaveReport 保存报表历史
func (s *ConfigStore) SaveReport(content string) error {
	historyDir := getHistoryDir()
	os.MkdirAll(historyDir, 0755)
	
	filename := time.Now().Format("20060102_150405") + ".json"
	filepath := filepath.Join(historyDir, filename)
	
	data, _ := json.Marshal(map[string]string{
		"content":   content,
		"timestamp": time.Now().Format(time.RFC3339),
	})
	
	return os.WriteFile(filepath, data, 0644)
}

func getHistoryDir() string {
	configDir := config.GetConfigDir()
	return filepath.Join(configDir, "report_history")
}
