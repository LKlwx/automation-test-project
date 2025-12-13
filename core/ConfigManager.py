import json
import os

# typing模块是Python 3.5引入的，用于类型注解，使用时必须导入具体的类型
from typing import Any, Dict


class ConfigManager:
    """
    一个通用的JSON配置管理器
    频繁读写原文件会很慢，所以使用内存缓存
    直接修改原文件可能导致文件损坏，所以不直接写回文件
    返回副本可以防止调用者意外修改内部数据
    """

    def __init__(self, file_name: str):  # 带类型注解写法，表示参数应该是一个字符串
        """
        初始化管理器
        """
        self.file_name = file_name
        self._config_data = None  # 内部变量，用于换粗配置数据
        self._load()  # 初始化时，自动加载配置文件

    def _load(self) -> None:  # -> None 表示这个方法没有返回值
        """
        从文件读取JSON数据到内存
        """
        # 1. 使用 open() 以读取模式打开 self.config_file_path
        # 2. 使用 json.load() 将文件内容加载为Python字典
        # 3. 将加载的字典赋值给 self._config_data
        with open(self.file_name, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            self._config_data = json_data

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项的值
        :param key: 配置键，如 'base_url'
        :param default: 如果键不存在，返回的默认值
        :return: 配置的值
        """
        # 直接从内存中的字典获取，避免每次读取文件
        return self._config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        设置(更新)配置项的值
        :param key: 配置键，如 'base_url'
        :param value: 新的配置值
        """
        # 直接在内存中的字典设置，避免每次写入文件
        self._config_data[key] = value
        # 立即将更新写回文件，调用self._save()
        self._save()

    def _save(self) -> None:
        """
        将内存中的配置数据写回文件
        使用 json.dump()，并考虑可读性（indent参数）。
        """
        # 1. 使用 open() 以写入模式打开 self.config_file_path
        # 2. 使用 json.dump() 将字典写入文件
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self._config_data, f, indent=4, ensure_ascii=False)

    def get_all(self) -> dict:
        """
        获取全局配置的副本
        :return: 配置字典
        """
        return self._config_data.copy()


if __name__ == "__main__":
    # 1. 创建管理器实例，传入您刚才创建的文件
    config = ConfigManager("config.json")

    # 2. 测试读取
    print("初始配置：")
    print(f"base_url: {config.get('base_url')}")
    print(f"timeout: {config.get('timeout')}")
    print(f"users: {config.get('users')}")
    print(f"不存在的键: {config.get('not_exist', '默认值')}")

    # 3. 测试更新并写回文件
    print("\n更新 timeout 为 30...")
    config.set("timeout", 30)
    print(f"新的timeout(内存中): {config.get('timeout')}")

    # 4. 验证文件是否真的被更新了（可以手动打开config.json文件查看）
    print("\n更新完成。请亲自打开 'config.json' 文件，检查 timeout 的值是否已变为 30。")
