import json
import os

# typing模块是Python 3.5引入的，用于类型注解，使用时必须导入具体的类型
# from typing import Any, Dict


class ConfigManager:
    """读取config目录下的config.json文件"""

    def __init__(self):
        self.config_path = os.path.join("config", "config.json")
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"config.json文件未找到: {self.config_path}")
        # 加载配置
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)
