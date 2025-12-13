#!/usr/bin/env python3
"""
自动化测试项目主程序
使用方式：
    python run.py                 # 运行所有测试
    python run.py --test api      # 只运行接口测试
    python run.py --test web      # 只运行Web测试
"""

import sys
import os
import argparse


def run_api_tests():
    """运行接口测试"""
    print("运行接口测试...")
    try:
        from tests.test_api import DataDrivenTest

        tester = DataDrivenTest()
        tester.run()
        return True
    except Exception as e:
        print(f"接口测试失败: {e}")
        return False


def run_web_tests():
    """运行Web测试"""
    print("运行Web测试...")
    try:
        from tests.test_web import BusinessFlowTest

        tester = BusinessFlowTest()
        tester.run("data/test_data.xlsx")
        return True
    except Exception as e:
        print(f"Web测试失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="运行自动化测试")
    parser.add_argument(
        "--test", choices=["api", "web", "all"], default="all", help="选择测试类型"
    )

    args = parser.parse_args()

    print(f"开始运行测试: {args.test}")

    if args.test in ["api", "all"]:
        run_api_tests()

    if args.test in ["web", "all"]:
        run_web_tests()

    print("测试完成！")


if __name__ == "__main__":
    main()
