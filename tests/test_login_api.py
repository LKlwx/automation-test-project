import pytest
import allure
from core.data_reader import DataReader

data_reader = DataReader()


@allure.feature("登录接口测试")
@allure.story("基于httpbin.org模拟登录")
@pytest.mark.login
class TestLoginApi:

    @allure.title("admin账号模拟登录")
    def test_login_admin(self, api_client):
        response = api_client.login("admin", "admin123")
        assert response.status_code == 200
        assert response.json()["json"]["username"] == "admin"
        assert response.json()["json"]["user_type"] == "admin"

    @allure.title("guest账号模拟登录")
    def test_login_user(self, api_client):
        response = api_client.login("guest", "guest123")
        assert response.status_code == 200
        assert response.json()["json"]["username"] == "guest"
        assert response.json()["json"]["user_type"] == "guest"

    # 从Excel中批量读取数据
    @allure.title("Excel批量用例")
    @pytest.mark.parametrize("user", data_reader.read_excel())
    def test_login_excel(self, api_client, user):
        # 动态设置标题,直接从字典中取description
        desc = user["description"]
        allure.dynamic.title(f"Excel批量用例:{desc}")
        # 处理用户,密码为空的情况
        username = user["username"] if user["username"] is not None else ""
        password = user["password"] if user["password"] is not None else ""

        response = api_client.login(username, password)
        if user["expected_status"] == 200:
            assert response.status_code == 200
        else:
            pytest.xfail(
                f"httpbin.org不返回{user['expected_status']},真实接口需要验证状态码"
            )

        assert response.json()["json"]["username"] == username
        assert response.json()["json"]["password"] == password
        print(f"用例描述:{user['description']},用户名:{username}")

    @allure.title("json文件批量用例")
    @pytest.mark.parametrize("user", data_reader.read_json()["users"])
    def test_login_json(self, api_client, user):
        # 动态设置标题,直接从字典中取description
        desc = user["description"]
        allure.dynamic.title(f"json文件批量用例:{desc}")
        # 处理用户,密码为空的情况
        username = user["username"] if user["username"] is not None else ""
        password = user["password"] if user["password"] is not None else ""

        response = api_client.login(username, password)
        if user["expected_status"] == 200:
            assert response.status_code == 200
        else:
            pytest.xfail(
                f"httpbin.org不返回{user['expected_status']},真实接口需要验证状态码"
            )
        assert response.json()["json"]["username"] == username
        assert response.json()["json"]["password"] == password
        print(f"用例描述:{user['description']},用户名:{username}")