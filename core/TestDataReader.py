import openpyxl
import json

class TestDataReader:
    """
    一个从Excel读取测试数据的通用读取器
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.workbook = openpyxl.load_workbook(self.file_name)
        # 一个Excel文件中可能包含多个sheet，通常不在这里指定
        # self.sheet = self.wb.active

    def read_data_by_sheet(self, sheet_name):
        """
        根据sheet名读取数据，并转换为字典列表
        """
        sheet = self.workbook[sheet_name]
        # 获取第一行数据作为key
        keys = [cell.value for cell in sheet[1]]
        # 获取数据
        values = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # 将标题和每行数据打包成字典
            row_dict = dict(zip(keys, row))
            values.append(row_dict)
        return values

    # 根据题目6补充一个方法，从JSON中读取数据
    def read_data_by_json(self, json_file):
        """读取JSON文件中的数据"""
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def read_data_by_username(self, username, sheet_name="Login"):
        """
            能根据 username 为 key，快速取出对应行的所有测试数据
        """
        data = self.read_data_by_sheet(sheet_name)
        for row in data:
            if row["username"] == username:
                return row
        # 如果找到了，就返回数据，否则返回None
        return None


if __name__ == "__main__":
    local_reader = TestDataReader("test_data.xlsx")
    all_data = local_reader.read_data_by_sheet("Login")
    print(f"所有数据：{all_data}")
    user_data = local_reader.read_data_by_username("test1")
    print(f"用户test1数据：{user_data}")
