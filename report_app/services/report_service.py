"""报表生成服务"""
import json
from datetime import datetime


class ReportService:
    def __init__(self, config):
        self.config = config
    
    def generate_report(self, data):
        """生成报表文本"""
        lines = []
        
        lines.append(f"1.单位名称：{data.get('unit_name', '')}")
        lines.append(f"2.日期：{data.get('date', '')}")
        lines.append(f"3.所在区域：{data.get('region', '')}")
        
        # 人员情况
        chinese_total = self.config.get('chinese_count', 14) + 1
        local_count = self.config.get('local_count', 29)
        soldier_count = self.config.get('soldier_count', 8)
        manager_name = self.config.get('manager_name', '赵铁寨')
        unit_name = self.config.get('unit_name', 'Rig919')
        
        personnel = f"中方人员{chinese_total}人（其中{unit_name}{chinese_total - 1}人，外聘厨师 3 人，基地经理 1 人）"
        personnel += f"{unit_name}当地雇员{local_count}人；士兵{soldier_count}人"
        personnel += f"，基地经理{manager_name}驻井指导工作。"
        
        lines.append(f"4.人员情况：{personnel}")
        lines.append(f"5.生活物资储备天数：{self.config.get('supply_days', 30)}天；井场柴油{self.config.get('diesel_volume', 50)}方，可用{self.config.get('diesel_days', 15)}天。")
        lines.append(f"6.井号：{self.config.get('well_name', '')} 设计井深：{self.config.get('design_depth', 1000)} m")
        lines.append(f"7.今日工况：{data.get('today_work', '')}。")
        lines.append(f"8.当前井深：{data.get('current_depth', 0)}m")
        lines.append(f"9.下步工况：{data.get('next_work', '')}。")
        
        comm = f"{self.config.get('comm_status', '')}，平台经理：{self.config.get('manager_phone', '')} Thuraya 电话：{self.config.get('thuraya_phone', '')}卫星网络座机：6660353（内线）021-80246760（外线）安全情况：{self.config.get('security_status', '')}"
        lines.append(f"10.通讯情况：{comm}")
        
        return "\n".join(lines)
