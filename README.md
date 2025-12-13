# 自动化测试项目
包含接口自动化和Web自动化的完整框架。

## 🛠 技术栈
- Python + requests（接口测试）
- Selenium + Page Object Model（Web测试）
- 数据驱动测试（Excel/JSON数据源）

## 项目结构
- `core/` - 核心工具类（数据读取、配置管理、HTTP客户端）
- `pages/` - 页面对象模型（POM设计模式）
- `tests/` - 测试用例（接口测试、Web测试）
- `data/` - 测试数据（Excel/JSON格式）
- `config/` - 配置文件

## 使用方法
```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
python run.py

# 只运行接口测试
python run.py --test api

# 只运行Web测试
python run.py --test web