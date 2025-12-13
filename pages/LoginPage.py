"""
题目5：页面操作封装
目标：为任何一个常用网站（如 知乎、GitHub）的一个页面（如登录页）创建 Page Object 类。
要求：
定义 LoginPage 类，在 __init__ 中定位页面核心元素（用户名输入框、密码输入框、登录按钮）。
封装 input_username(), input_password(), click_submit() 方法。
封装一个 login() 方法，接收用户名和密码，组合完成整个登录流程。
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginPage:
    def __init__(self, driver, url=None) -> None:
        """
        初始化登录界面
        param driver:WebDriver实例
        param url:登录页面的url
        """
        self.driver = driver  # 将传入的WebDriver实例赋值给类的driver属性
        self.username_input = (By.ID, "login_field")  # 用户名输入框 - 使用ID定位方式
        self.password_input = (By.ID, "password")  # 密码输入框 - 使用ID定位方式
        self.submit_button = (By.NAME, "commit")  # 登录按钮 - 使用NAME定位方式
        if url:  # 如果提供了url参数
            self.driver.get(url)  # 导航到指定的登录页面
            print(f"已导航到:{url}")  # 打印导航信息
        # else:
        #     self.driver.get("https://github.com/login")

    def input_username(self, username) -> None:
        """
        输入用户名
        param username:用户名
        """
        try:
            username = str(username)
            print(f"开始输入用户名:{username}")
            # 等待用户名输入框出现
            username_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.username_input)
            )
            # 清空输入框
            username_element.clear()
            # 输入用户名
            username_element.send_keys(username)
            print(f"已输入用户名:{username}")
        except Exception as e:
            print(f"输入用户名失败:{e}")
            raise

    def input_password(self, password) -> None:
        """
        输入密码
        param password:密码
        """
        try:
            password = str(password)
            print(f"开始输入密码:{password}")
            # 等待密码输入框出现
            password_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.password_input)
                # presence_of_element_located：只检查元素是否存在于DOM中
                # EC.presence_of_element_located(self.password_input)
            )
            # 先点击一下输入框，确保被激活
            password_element.click()
            time.sleep(1)
            # 清空输入框
            password_element.clear()
            # 输入密码
            password_element.send_keys(password)
            print(f"已输入密码,长度为{len(password)}位")
        except Exception as e:
            print(f"输入密码失败:{e}")
            raise

    def click_submit(self) -> None:
        """
        点击登录按钮
        """
        try:
            print(f"开始点击登录按钮")
            # 等待登录按钮出现
            submit_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.submit_button)
            )
            # 点击登录按钮
            submit_element.click()
            print(f"已点击登录按钮")

            # 等待页面有变化（例如等待结果出现）
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element(By.ID, "result").text != ""
            )
        except Exception as e:
            print(f"点击登录按钮失败:{e}")
            raise

    def login(self, username, password) -> None:
        """
        完整的登录流程 - 题目要求的方法4
        组合调用input_username、input_password、click_submit
        :param username: 用户名
        :param password: 密码
        """
        print(f"\n{'='*50}")
        print(f"开始登录流程")
        print(f"用户名: {username}")
        print(f"{'='*50}")
        try:
            # 输入用户名
            self.input_username(username)
            # 输入密码
            self.input_password(password)
            # 点击登录按钮
            self.click_submit()
            print(f"{'='*50}")
            print("登录流程执行完毕")
            print(f"{'='*50}")
        except Exception as e:
            print(f"登录流程执行失败:{e}")
            raise


if __name__ == "__main__":
    driver = webdriver.Edge()

    try:
        # 创建LoginPage实例
        login_page = LoginPage(driver, "https://github.com/login")

        # 测试1:分别调用三个方法
        print("\n测试1:分别调用三个方法")
        login_page.input_username("username")
        login_page.input_password("password")
        login_page.click_submit()

        print("\n等待3s回到登录页面")
        time.sleep(3)

        # 重新打开登录页面
        driver.get("https://github.com/login")
        time.sleep(2)
        login_page = LoginPage(driver)
        # 测试2:调用login方法
        print("\n测试2：使用login()组合方法")
        login_page.login("another_user", "another_password")

        print("\n所有测试完成！")
    except Exception as e:
        print(f"测试过程中存在错误{e}")
    finally:
        # 关闭浏览器
        time.sleep(3)
        driver.quit()
        print("浏览器已关闭")
