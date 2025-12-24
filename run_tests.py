import subprocess
import os
import shutil

# 获取项目根目录绝对路径
project_root = os.path.dirname(os.path.abspath(__file__))
# 单独定义Allure报告目录
allure_results_dir = os.path.join(project_root, "reports", "allure-results")


def clean_reports():
    """清理旧的Allure报告和日志"""
    if os.path.exists("reports/allure-results"):
        shutil.rmtree("reports/allure-results")
    os.makedirs("reports/allure-results", exist_ok=True)
    print("已清理旧报告，创建新的报告目录")


def run_tests():
    """运行并生成Allure报告"""
    clean_reports()
    # 运行pytest，指定测试文件
    pytest_cmd = [
        "pytest",
        "tests/test_login_api.py",
        "-v",
        "-s",
        f"--rootdir={project_root}",
        "--alluredir",  # 参数名单独分离
        allure_results_dir,  # 参数值单独分离
    ]
    subprocess.run(
        pytest_cmd,
        check=True,
        cwd=project_root,
        # Windows必需：通过系统shell解析参数
        shell=True,
    )

    # 打开Allure报告
    allure_cmd = [
        "allure",
        "serve",
        allure_results_dir,
    ]
    subprocess.run(
        allure_cmd,
        cwd=project_root,
        check=True,
        shell=True,
    )


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"测试运行失败：{str(e)}")
