"""
登录页面对象（示例）
"""
from Common.baseView import BasePage
from typing import Union, Tuple
from config.environments import env_manager


class LoginPageLocators:
    """登录页面定位器"""
    # 使用 CSS 选择器
    USERNAME_INPUT = "#username-input"
    PASSWORD_INPUT = "#password-input"
    
    # 使用角色定位
    LOGIN_BUTTON = ("role", "button", "Login")
    
    # 使用文本定位
    ERROR_MESSAGE = ("text", "登录失败")
    
    # 使用占位符定位（示例）
    # USERNAME_INPUT = ("placeholder", "请输入用户名")


class LoginPage(BasePage):
    """登录页面对象"""
    
    def goto(self, base_url: str = None):
        """
        打开登录页面
        
        Args:
            base_url: 基础URL，如果为None则从配置读取
        """
        if base_url is None:
            base_url = env_manager.get_base_url()
        self.page.goto(f"{base_url}/login")
        self.page.wait_for_load_state("networkidle")
    
    def login(self, username: str, password: str):
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        # 输入用户名
        self.find(LoginPageLocators.USERNAME_INPUT).fill(username)
        
        # 输入密码
        self.find(LoginPageLocators.PASSWORD_INPUT).fill(password)
        
        # 点击登录按钮
        self.find(LoginPageLocators.LOGIN_BUTTON).click()
        
        # 等待登录完成
        self.page.wait_for_load_state("networkidle")
    
    def get_error_message(self) -> str:
        """
        获取错误消息（如果存在）
        
        Returns:
            str: 错误消息文本，如果不存在则返回空字符串
        """
        try:
            error_element = self.find(LoginPageLocators.ERROR_MESSAGE)
            if error_element.is_visible():
                return error_element.text_content().strip()
        except Exception:
            pass
        return ""
    
    def is_logged_in(self) -> bool:
        """
        判断是否已登录（根据实际业务逻辑调整）
        
        Returns:
            bool: 是否已登录
        """
        # 示例：检查是否存在登录后的特征元素
        # 实际使用时需要根据业务调整
        try:
            # 假设登录后会跳转到首页，且首页有特定的元素
            # self.find("#user-menu").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
