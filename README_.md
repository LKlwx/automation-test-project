# 自动化测试项目
基于Python+Pytest+Allure实现了登录接口自动化测试，支持 Excel/JSON 双数据驱动，已完成全量测试用例执行
Web自动化测试还未完成，后续会继续完善
  
# 项目结构
automation-test-project/
├── config/                  # 配置目录
│   └── config.json          # 接口基础配置
├── core/                    # 核心工具包
│   ├── __init__.py
│   ├── api_client.py        # HTTP请求封装（含日志、会话保持）
│   ├── config_manager.py    # 配置读取与管理
│   └── data_reader.py       # 测试数据解析工具
├── data/                    # 测试数据目录
│   ├── test_data.json       # JSON格式测试数据
│   └── test_data.xlsx       # Excel格式测试数据
├── logs/                    # 日志目录
│   └── apilog               # 接口请求日志
├── pages/                   
│   └── login_page.py        # 未作修改
├── reports/                 # 测试报告（自动生成）
│   └── allure-results       # Allure原始报告数据
├── tests/                   # 测试用例目录
│   ├── __init__.py
│   ├── conftest.py          # Pytest夹具配置
│   ├── test_login_api.py    # 登录接口测试用例
│   └── test_web.py          # 未作修改
|   └── test_login.html      # 未作修改
├── .gitignore               # Git忽略规则
├── pytest.ini               # Pytest配置文件
├── requirements.txt         # 项目依赖清单
├── run_tests.py             # 测试执行入口
└── README.md                # 项目说明
  
# 项目更新内容
1. 文件命名规范
    对核心请求、配置、数据解析模块进行了命名规范和
  