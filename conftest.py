"""
Pytest & Playwright 核心 fixture 与钩子
"""
import pytest
import allure
from playwright.sync_api import Page, BrowserContext, Browser
from typing import Generator
import os
from datetime import datetime
from pathlib import Path

# 导入环境管理器
from config.environments import env_manager


# ==================== Pytest 配置钩子 ====================

def pytest_configure(config):
    """
    Pytest 配置钩子：注册 markers 和设置元数据
    """
    # 注册自定义 markers
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试用例"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试用例"
    )
    config.addinivalue_line(
        "markers", "functional: 功能测试用例"
    )
    config.addinivalue_line(
        "markers", "api: API 测试用例"
    )
    config.addinivalue_line(
        "markers", "ui: UI 测试用例"
    )
    
    # 设置 Allure 元数据
    allure.dynamic.label("framework", "Playwright + Pytest")
    allure.dynamic.label("language", "Python")
    allure.dynamic.label("executor", os.getenv("USER", "unknown"))
    allure.dynamic.label("environment", env_manager.get_current_environment())


def pytest_sessionstart(session):
    """
    测试会话开始时的钩子
    """
    session.start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"测试会话开始时间: {session.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"当前环境: {env_manager.get_current_environment()}")
    print(f"{'='*60}\n")
    
    # 创建必要的目录
    log_config = env_manager.get_logging_config()
    log_dir = log_config.get("log_dir", "tests/logs")
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    report_config = env_manager.get_report_config()
    allure_results_dir = report_config.get("allure_results_dir", "tests/reports/allure-results")
    Path(allure_results_dir).mkdir(parents=True, exist_ok=True)


def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束时的钩子
    """
    if hasattr(session, 'start_time'):
        end_time = datetime.now()
        duration = end_time - session.start_time
        print(f"\n{'='*60}")
        print(f"测试会话结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总耗时: {duration}")
        print(f"退出状态: {exitstatus}")
        print(f"{'='*60}\n")


# ==================== 测试报告增强钩子 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试报告生成钩子：处理测试结果、截图等
    """
    outcome = yield
    rep = outcome.get_result()
    
    # 将测试函数的 docstring 作为 Allure 描述
    if item.function.__doc__:
        allure.dynamic.description(item.function.__doc__)
    
    # 失败时自动截图
    if rep.when == "call" and rep.failed:
        # 获取 page fixture（如果存在）
        if "page" in item.fixturenames:
            page = item.funcargs.get("page")
            if page:
                try:
                    # 截图并附加到 Allure
                    screenshot = page.screenshot(full_page=True)
                    allure.attach(
                        screenshot,
                        name="失败截图",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                    # 如果配置了视频录制，也可以在这里处理
                    report_config = env_manager.get_report_config()
                    if report_config.get("video_on_failure", False):
                        # 视频处理逻辑（需要额外实现）
                        pass
                except Exception as e:
                    print(f"截图失败: {e}")


# ==================== Browser & Context Fixtures ====================

@pytest.fixture(scope="session")
def browser_launch_args():
    """
    浏览器启动参数（session 作用域）
    从环境管理器读取浏览器配置
    """
    browser_config = env_manager.get_browser_config()
    return {
        "headless": browser_config.get("headless", True),
        "slow_mo": browser_config.get("slow_mo", 0),
    }


@pytest.fixture(scope="class")
def context_args(browser_launch_args):
    """
    浏览器上下文参数（class 作用域）
    在浏览器参数基础上补充 viewport 等
    """
    browser_config = env_manager.get_browser_config()
    viewport = browser_config.get("viewport", {"width": 1920, "height": 1080})
    
    return {
        **browser_launch_args,
        "viewport": viewport,
    }


@pytest.fixture(scope="class")
def context(context_args, browser_type_launch_args, browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    浏览器上下文（class 作用域）
    覆盖 pytest-playwright 默认 context，使其按 class 作用域复用
    """
    browser_config = env_manager.get_browser_config()
    viewport = browser_config.get("viewport", {"width": 1920, "height": 1080})
    
    context = browser.new_context(
        viewport=viewport,
        **browser_type_launch_args
    )
    
    # 设置默认超时时间
    timeout = browser_config.get("timeout", 30000)
    context.set_default_timeout(timeout)
    context.set_default_navigation_timeout(
        browser_config.get("navigation_timeout", 60000)
    )
    
    yield context
    context.close()


# ==================== Page Fixtures ====================

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    页面实例（function 作用域）
    每个测试函数一个新 Page
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="class")
def class_page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    类级别页面实例（class 作用域）
    每个测试类一个 Page，适合一页多断言的场景
    """
    page = context.new_page()
    yield page
    page.close()


# ==================== 业务状态 Fixtures ====================

@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    """
    已登录页面 fixture
    在 fixture 内执行登录流程，返回已登录状态的 Page
    
    注意：这是一个示例 fixture，需要根据实际业务实现登录逻辑
    """
    from pages.login_page import LoginPage
    
    # 获取账号信息
    account = env_manager.get_account()
    base_url = env_manager.get_base_url()
    
    # 执行登录
    login_page = LoginPage(page)
    login_page.goto(base_url)
    login_page.login(
        username=account.get("username", ""),
        password=account.get("password", "")
    )
    
    # 等待登录完成（根据实际情况调整）
    page.wait_for_load_state("networkidle")
    
    return page


# ==================== API 测试辅助逻辑（可选）====================

def pytest_configure_node(node):
    """
    节点配置钩子（用于分布式测试）
    """
    pass


def pytest_collection_modifyitems(config, items):
    """
    收集测试用例后的钩子
    可以在这里对测试用例进行过滤、排序等操作
    """
    # 示例：根据命令行参数过滤 API 测试
    if config.getoption("--api-only", default=False):
        # 只运行标记为 api 的测试
        for item in items:
            if "api" not in [mark.name for mark in item.iter_markers()]:
                item.add_marker(pytest.mark.skip(reason="只运行 API 测试"))


def pytest_addoption(parser):
    """
    添加自定义命令行选项
    """
    parser.addoption(
        "--api-only",
        action="store_true",
        default=False,
        help="只运行 API 测试"
    )
    parser.addoption(
        "--ui-only",
        action="store_true",
        default=False,
        help="只运行 UI 测试"
    )
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="指定测试环境（dev/staging/prod）"
    )


def pytest_collection_finish(session):
    """
    测试用例收集完成后的钩子
    如果指定了环境，在这里设置
    """
    env_option = session.config.getoption("--env")
    if env_option:
        env_manager.set_environment(env_option)
        print(f"已切换到环境: {env_option}")
