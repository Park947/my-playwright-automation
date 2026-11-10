"""
UI 自动化测试用例示例
"""
import pytest
from playwright.sync_api import expect
from pages.example_page import ExamplePage
from config.environments import env_manager


class TestExample:
    """示例测试类"""
    
    @pytest.mark.ui
    @pytest.mark.functional
    def test_example_search(self, page):
        """
        测试搜索功能
        
        验证搜索功能是否正常工作
        """
        # 创建页面对象
        example_page = ExamplePage(page)
        
        # 打开页面
        base_url = env_manager.get_base_url()
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # 执行搜索
        keyword = "test"
        example_page.search(keyword)
        
        # 获取第一个结果
        first_result = example_page.get_first_result_text()
        
        # 断言
        assert keyword.lower() in first_result.lower(), f"搜索结果中应包含 '{keyword}'"
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_example_menu(self, page):
        """
        测试菜单功能
        
        验证菜单是否可以正常打开
        """
        example_page = ExamplePage(page)
        
        base_url = env_manager.get_base_url()
        page.goto(base_url)
        page.wait_for_load_state("networkidle")
        
        # 打开菜单
        example_page.open_menu()
        
        # 验证菜单已打开（根据实际业务调整断言）
        # 例如：检查菜单元素是否可见
        # expect(page.locator(".menu-panel")).to_be_visible()


@pytest.mark.ui
@pytest.mark.functional
def test_example_single_function(page):
    """
    单个函数形式的测试用例示例
    """
    example_page = ExamplePage(page)
    
    base_url = env_manager.get_base_url()
    page.goto(base_url)
    
    # 执行操作
    example_page.search("example")
    
    # 使用 Playwright 的 expect 进行断言
    expect(page.locator(".search-result-item")).to_have_count(1, timeout=5000)
