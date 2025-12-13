import sys
import os
import json

# 修改导入路径
from core.TestDataReader import TestDataReader
from core.ApiClient import ApiClient


class DataDrivenTest:
    """
    1.使用题目1的TestDataReader读取测试数据
    2.使用题目3的ApiClient调用接口
    3.循环测试所有数据并断言结果
    """

    def __init__(self):
        # 修改文件路径
        excel_path = os.path.join("data", "test_data.xlsx")
        config_path = os.path.join("config", "config.json")

        print(f"Excel:{excel_path}")
        print(f"Config:{config_path}")

        # 创建TestDataReader实例
        self.tdr = TestDataReader(excel_path)
        # 创建ApiClient实例
        self.ac = ApiClient(config_path)

    def run(self):
        """运行所有测试"""
        # 使用题目1读取Excel表格数据
        test_cases = self.tdr.read_data_by_sheet("Login")
        print(f"读取到{len(test_cases)}条测试数据")

        if not test_cases:
            print("没有测试数据")
            return

        # 循环嗲用ApiClient的login方法,enumerate()函数返回索引和值
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试用例{i}：{test_case}")

            # 使用get方法获取避免KeyError
            username = test_case.get("username", "")
            password = test_case.get("password", "")
            expected_status_str = test_case.get("expected_status", "")

            # 检查必填字段是否为空
            if not username:
                print(f"测试用例缺少用户名")
                continue
            if not password:
                print(f"{username}缺少密码")
                continue
            if not expected_status_str:
                print(f"{username}缺少预期状态码")
                continue
            try:
                # 调用登录接口
                response = self.ac.login(username, password)
                status_code = response.status_code
                # print(f"状态码：{status_code}")

                # 断言响应状态码
                expected_status = int(expected_status_str)
                # 使用Excel中的expected_status字段作为预期状态码

                if status_code == expected_status:
                    print(f"用户{username}预期状态码为：{expected_status}测试通过")
                else:
                    print(
                        f"用户{username}预期状态码为：{expected_status}测试失败,实际状态码为：{status_code}"
                    )
            except ValueError:
                print(f"预期状态码{expected_status_str}不是有效数字")
            except Exception as e:
                print(f"测试用例{i}执行失败：{str(e)}")


# 运行测试
if __name__ == "__main__":
    print("开始执行测试")
    print("=" * 50)

    tester = DataDrivenTest()
    tester.run()

    print("\n" + "=" * 50)
    print("测试完成")
