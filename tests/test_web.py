"""
题目6：结合业务的流程测试
目标：结合题目5和第三方数据。
要求：
从 Excel 或 JSON 文件中读取一组用户名和密码。
编写脚本，使用 LoginPage 类，循环尝试这组数据登录。
登录后，判断页面跳转或出现的提示信息，来判断登录成功或失败，并记录结果。
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pages.LoginPage import LoginPage
from core.TestDataReader import TestDataReader



class BusinessFlowTest:
    """业务流程测试"""

    def __init__(self):
        self.driver = webdriver.Edge()
        # 窗口最大化
        self.driver.maximize_window()

    def load_test_data(self, file_name):
        """加载测试数据，支持Excel和JSON文件"""
        if not os.path.exists(file_name):
            raise Exception(f"文件{file_name}不存在")

        # os.path.splitext(file_name)返回一个元组，第一个元素是文件名，第二个元素是文件扩展名
        # [1]取第二个元素，lower()转小写
        file_ext = os.path.splitext(file_name)[1].lower()

        if file_ext == ".xlsx":
            # 用TestDataReader读取Excel
            reader = TestDataReader(file_name)
            test_cases = reader.read_data_by_sheet("Login")
            return test_cases
        elif file_ext == ".json":
            # 读取JSON文件
            reader = TestDataReader(file_name)
            data = reader.read_data_by_json(file_name)

            # 从json中读取user
            if isinstance(data, dict) and "users" in data:
                users = data["users"]
                # 为每个用户添加expected_status（因为你的JSON里没有这个字段）
                for user in users:
                    user["expected_status"] = "200"  # 默认都预期成功
                return users
            else:
                # 格式正确，直接返回
                return data
        else:
            raise Exception(f"不支持的文件类型{file_ext}")

    def run(self, file_name):
        """运行测试"""
        print(f"开始测试流程,文件:{file_name}")

        # 加载数据
        test_cases = self.load_test_data(file_name)
        if not test_cases:
            print("没有测试用例，退出")
            return
        else:
            print(f"读取到{len(test_cases)}条测试用例")

        # 循环测试
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试用例{i}:{test_case}")

            username = test_case.get("username")
            password = test_case.get("password")

            if not username or not password:
                print("用户名或密码为空，跳过该条用例")
                results.append(f"用例{i}:{test_case}，有空数据，跳过")
                continue

            try:
                # HTML文件现在应该在tests目录下
                html_path = os.path.join("tests", "test_login.html")

                # 如果不在tests目录，尝试当前目录
                if not os.path.exists(html_path):
                    html_path = "test_login.html"

                print(f"HTML文件路径: {html_path}")
                print(f"HTML文件存在: {os.path.exists(html_path)}")

                if not os.path.exists(html_path):
                    print(f"找不到html文件:{html_path}")
                    results.append(f"用例{i}: {username} - 错误: 找不到HTML文件")
                    continue

                # 创建LoginPage时传入本地文件路径
                login_page = LoginPage(
                    self.driver, url=f"file:///{os.path.abspath(html_path)}"
                )
                print(f"打开登录页面:{html_path}")
                time.sleep(2)

                # 记录原始文件
                original_url = self.driver.current_url

                # 使用LoginPage类进行登录
                login_page.login(username, password)
                time.sleep(3)

                # 判断登录结果
                # 直接检查result元素的文本
                try:
                    result_div = self.driver.find_element(By.ID, "result")
                    result_text = result_div.text

                    if "登录成功" in result_text:
                        result_msg = f"用例{i}: {username} - 登录成功"
                    elif "用户名或密码错误" in result_text:
                        result_msg = f"用例{i}: {username} - 登录失败"
                    else:
                        # 如果上面的判断都不匹配，检查URL
                        current_url = self.driver.current_url
                        if current_url != original_url:
                            result_msg = f"用例{i}: {username} - 登录成功,页面跳转"
                        else:
                            result_msg = f"用例{i}: {username} - 登录失败,未知错误"

                except NoSuchElementException as e:
                    print(f"未找到result元素: {e}")
                    # 如果找不到result元素，检查URL是否变化
                    current_url = self.driver.current_url
                    if current_url != original_url:
                        result_msg = f"用例{i}: {username} - 登录成功（触发跳转）"
                    else:
                        # 兜底：检查页面源码
                        page_source = self.driver.page_source
                        if "登录成功" in page_source:
                            result_msg = f"用例{i}: {username} - 登录成功"
                        elif "用户名或密码错误" in page_source:
                            result_msg = f"用例{i}: {username} - 登录失败"
                        else:
                            result_msg = f"用例{i}: {username} - 无法判断结果"
                print(result_msg)
                results.append(result_msg)

                # 如果不是最后一个,刷新准备下一个
                if i < len(test_cases):
                    print("刷新页面，准备下一个")
                    self.driver.refresh()
                    time.sleep(2)

            except Exception as e:
                error_msg = f"用例{i}: {username} - 异常: {str(e)[:50]}"
                print(f"登录流程执行失败: {e}")
                results.append(error_msg)

                # 如果出现异常，重新打开浏览器
                try:
                    self.driver.quit()
                    self.driver = webdriver.Edge()
                    self.driver.maximize_window()
                except:
                    pass

        # 显示最终结果
        print("\n" + "=" * 60)
        print("测试结果汇总:")
        print("=" * 60)
        for result in results:
            print(result)


if __name__ == "__main__":
    # 测试数据文件现在在data目录下
    file_name = os.path.join("data", "test_data.xlsx")

    # 检查文件是否存在
    if not os.path.exists(file_name):
        print(f"错误: 找不到测试数据文件 {file_name}")
        print("请确保test_data.xlsx在data目录下")
        exit(1)

    test = BusinessFlowTest()
    try:
        test.run(file_name)
    except Exception as e:
        print(f"测试失败: {e}")
    finally:
        time.sleep(3)
        test.driver.quit()
        print("测试结束")
