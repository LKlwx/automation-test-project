import requests
import logging
import os

# 日志初始化,日志文件存储在logs目录下
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class APIClient:
    """API客户端,基于config.json配置文件中的base_url和timeout"""

    def __init__(self) -> None:
        from .config_manager import ConfigManager

        self.config = ConfigManager()
        self.base_url = self.config.get("base_url")
        self.timeout = self.config.get("timeout", 30)
        self.session = requests.Session()
        logger.info(
            f"API客户端初始化完成,base_url:{self.base_url},timeout:{self.timeout}"
        )

    def login(self, username, password):
        """/post模拟登录接口"""
        login_url = f"{self.base_url}/post"
        # 防止config中无users字段
        admin_users = self.config.get("users", [])
        user_type = "admin" if username in admin_users else "guest"
        payload = {
            "username": username,
            "password": password,
            "user_type": user_type,
        }
        try:
            logger.info(f"模拟登录请求:{username}")
            # 发送post请求
            response = self.session.post(login_url, json=payload, timeout=self.timeout)
            logger.info(f"登录响应状态码:{response.status_code}")
            return response
        except Exception as e:
            logger.error(f"模拟登录请求失败:{str(e)}", exc_info=True)
            raise e
