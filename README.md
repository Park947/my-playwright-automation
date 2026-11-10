# my-playwright-automation

这是一个基于 Playwright 和 Pytest 的通用自动化测试框架，支持 UI 和 API 自动化测试。

## 框架特性

- ✅ **UI 自动化**：基于 Playwright 的页面自动化测试
- ✅ **API 测试**：基于 requests 的接口自动化测试
- ✅ **Page Object Model (POM)**：页面对象模式，代码复用性高
- ✅ **环境管理**：支持多环境配置（dev/staging/prod）
- ✅ **Allure 报告**：美观的测试报告
- ✅ **通知推送**：支持钉钉、邮件通知
- ✅ **统一日志**：完善的日志记录系统

## 目录结构

```
my-playwright-automation/
├── Common/                  # 通用基类 & 驱动封装
│   ├── baseView.py          # 页面基类
│   ├── caps.py              # 浏览器启动封装
│   └── __init__.py
├── config/                  # 配置 & 环境管理
│   ├── environments.py      # 环境管理器
│   ├── settings.yaml        # 配置文件
│   └── __init__.py
├── pages/                   # Page Object 层
│   ├── login_page.py        # 登录页面对象（示例）
│   ├── example_page.py      # 示例页面对象
│   └── __init__.py
├── tests/                   # 测试用例层
│   ├── test_ui/             # UI 自动化用例
│   ├── test_api/            # 接口自动化用例
│   ├── logs/                # 测试日志
│   └── reports/             # 测试报告
├── utils/                   # 工具与辅助模块
│   ├── helper_methods.py    # 日志、通用工具函数
│   ├── custom_assertions.py # 自定义断言
│   ├── resultPush.py        # 通知/推送
│   └── __init__.py
├── reports/                 # 报告配置
│   ├── conftest_report.py
│   └── custom_report_style.css
├── conftest.py              # Pytest 核心 fixture
├── pytest.ini               # Pytest 配置
├── requirements.txt         # 依赖声明
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 2. 配置环境

编辑 `config/settings.yaml`，配置你的测试环境信息：

```yaml
environments:
  dev:
    base_url: "https://dev.example.com"
    account:
      username: "your_username"
      password: "your_password"
```

### 3. 运行测试

```bash
# 运行全部测试
pytest

# 只运行 UI 测试
pytest tests/test_ui

# 只运行 API 测试
pytest -m "api" tests/test_api

# 运行冒烟测试
pytest -m "smoke"

# 指定浏览器
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# 有头模式（显示浏览器）
pytest --headed

# 指定环境
pytest --env staging
```

### 4. 查看报告

```bash
# 生成 Allure 报告
pytest --alluredir=tests/reports/allure-results

# 生成 HTML 报告
allure generate tests/reports/allure-results -o reports/allure-report --clean

# 打开报告
allure open reports/allure-report
```

## 使用指南

### 编写 Page Object

```python
from Common.baseView import BasePage

class MyPageLocators:
    BUTTON = "#my-button"
    INPUT = ("role", "textbox", "Name")

class MyPage(BasePage):
    def click_button(self):
        self.find(MyPageLocators.BUTTON).click()
    
    def fill_input(self, text: str):
        self.find(MyPageLocators.INPUT).fill(text)
```

### 编写测试用例

```python
import pytest
from pages.my_page import MyPage

@pytest.mark.ui
@pytest.mark.functional
def test_my_feature(page):
    my_page = MyPage(page)
    my_page.goto("https://example.com")
    my_page.click_button()
    # 断言...
```

### 定位器写法

框架支持多种定位方式：

- **CSS 选择器**：`"#login-btn"`, `".price-curr"`
- **角色定位**：`("role", "button", "Login")`
- **文本定位**：`("text", "Login")`
- **标签定位**：`("label", "Email")`
- **占位符定位**：`("placeholder", "请输入邮箱")`
- **测试ID定位**：`("testid", "login-button")`
- **XPath定位**：`("xpath", "//div[@id='xxx']")`

## 测试标记（Markers）

- `@pytest.mark.smoke` - 冒烟测试
- `@pytest.mark.regression` - 回归测试
- `@pytest.mark.functional` - 功能测试
- `@pytest.mark.api` - API 测试
- `@pytest.mark.ui` - UI 测试

## 环境变量

可以通过环境变量设置测试环境：

```bash
# Windows
set TEST_ENV=staging
pytest

# Linux/Mac
export TEST_ENV=staging
pytest
```

## 通知配置

在 `config/settings.yaml` 中配置钉钉或邮件通知：

```yaml
dingtalk:
  enabled: true
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
  keyword: "自动化测试"

email:
  enabled: true
  smtp_server: "smtp.example.com"
  # ...
```

## 注意事项

1. 首次运行前需要执行 `playwright install` 安装浏览器
2. 根据实际业务修改 `pages/` 中的页面对象
3. 根据实际环境修改 `config/settings.yaml` 配置
4. 测试用例中的断言需要根据实际业务调整

## 更多信息

详细框架设计说明请参考 `1.md` 文件。
