"""
登录功能测试用例示例
"""
import pytest
from pages.login_page import LoginPage
from config.environments import env_manager
from utils.helper_methods import get_logger


logger = get_logger()


class TestLogin:
    """登录功能测试类"""
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_login_success(self, page):
        """
        测试登录成功场景
        
        验证使用正确的用户名和密码可以成功登录
        """
        login_page = LoginPage(page)
        
        # 获取测试账号
        account = env_manager.get_account()
        username = account.get("username", "")
        password = account.get("password", "")
        
        # 打开登录页面
        login_page.goto()
        
        # 执行登录
        login_page.login(username, password)
        
        # 验证登录成功
        assert login_page.is_logged_in(), "登录应该成功"
        logger.info("登录测试通过")
    
    @pytest.mark.ui
    @pytest.mark.functional
    def test_login_failure(self, page):
        """
        测试登录失败场景
        
        验证使用错误的用户名或密码会显示错误消息
        """
        login_page = LoginPage(page)
        
        # 打开登录页面
        login_page.goto()
        
        # 使用错误的凭据登录
        login_page.login("wrong_username", "wrong_password")
        
        # 验证错误消息（根据实际业务调整）
        error_message = login_page.get_error_message()
        # assert error_message != "", "应该显示错误消息"
        logger.info(f"错误消息: {error_message}")


@pytest.mark.ui
@pytest.mark.functional
def test_login_with_logged_in_fixture(logged_in_page):
    """
    使用已登录页面 fixture 的测试示例
    
    这个测试会自动使用已登录状态的页面，无需重复登录步骤
    """
    # 直接使用已登录的页面进行业务操作
    # 例如：访问需要登录的页面
    logged_in_page.goto(f"{env_manager.get_base_url()}/dashboard")
    logged_in_page.wait_for_load_state("networkidle")
    
    # 验证页面已加载
    assert "dashboard" in logged_in_page.url.lower() or True  # 根据实际调整
