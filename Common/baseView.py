"""
BasePage 基类：封装 Playwright 定位与通用操作
提供统一的元素查找方法和通用页面操作
"""
from playwright.sync_api import Page, Locator
from typing import Union, List, Tuple, Any


class BasePage:
    """页面基类，封装 Playwright 定位与通用操作"""
    
    def __init__(self, page: Page):
        """
        初始化页面对象
        
        Args:
            page: Playwright Page 实例
        """
        self.page = page
    
    def find(self, locator: Union[str, Tuple[str, ...]]) -> Locator:
        """
        统一的元素查找入口，支持多种定位方式
        
        支持的定位方式：
        - 字符串：默认 CSS 选择器，如 "#login-btn", ".price-curr"
        - 元组：类型 + 值/选项
          - ("role", "button", "Buy Now") - 角色定位
          - ("text", "Login") - 文本定位
          - ("label", "Email") - 标签定位
          - ("placeholder", "请输入邮箱") - 占位符定位
          - ("testid", "login-button") - 测试ID定位
          - ("alt", "Logo") - alt属性定位
          - ("title", "Tooltip") - title属性定位
          - ("xpath", "//div[@id='xxx']") - XPath定位
        
        Args:
            locator: 定位器，可以是字符串（CSS选择器）或元组（类型+值）
        
        Returns:
            Locator: Playwright Locator 对象
        """
        if isinstance(locator, str):
            # 字符串：默认作为 CSS 选择器
            return self.page.locator(locator)
        elif isinstance(locator, tuple):
            locator_type = locator[0].lower()
            
            if locator_type == "role":
                # 角色定位：("role", "button", "Buy Now")
                role = locator[1]
                name = locator[2] if len(locator) > 2 else None
                return self.page.get_by_role(role, name=name)
            
            elif locator_type == "text":
                # 文本定位：("text", "Login")
                return self.page.get_by_text(locator[1], exact=False)
            
            elif locator_type == "label":
                # 标签定位：("label", "Email")
                return self.page.get_by_label(locator[1])
            
            elif locator_type == "placeholder":
                # 占位符定位：("placeholder", "请输入邮箱")
                return self.page.get_by_placeholder(locator[1])
            
            elif locator_type == "testid":
                # 测试ID定位：("testid", "login-button")
                return self.page.get_by_test_id(locator[1])
            
            elif locator_type == "alt":
                # alt属性定位：("alt", "Logo")
                return self.page.get_by_alt_text(locator[1])
            
            elif locator_type == "title":
                # title属性定位：("title", "Tooltip")
                return self.page.get_by_title(locator[1])
            
            elif locator_type == "xpath":
                # XPath定位：("xpath", "//div[@id='xxx']")
                return self.page.locator(locator[1])
            
            else:
                raise ValueError(f"不支持的定位器类型: {locator_type}")
        else:
            raise TypeError(f"定位器必须是字符串或元组，当前类型: {type(locator)}")
    
    def finds(self, locator: Union[str, Tuple[str, ...]]) -> Locator:
        """
        返回一组元素（列表语义），常用 self.find(...).nth(i)
        
        Args:
            locator: 定位器
        
        Returns:
            Locator: Playwright Locator 对象（可用于 nth() 等操作）
        """
        return self.find(locator)
    
    def close_popup_if_exists(self, popup_locator: Union[str, Tuple[str, ...]] = None, 
                              close_button_locator: Union[str, Tuple[str, ...]] = None):
        """
        根据约定的定位器尝试关闭通用弹窗
        
        Args:
            popup_locator: 弹窗定位器，如果为None则尝试通用弹窗选择器
            close_button_locator: 关闭按钮定位器，如果为None则尝试通用关闭按钮
        """
        try:
            if popup_locator is None:
                # 尝试常见的弹窗选择器
                common_popups = [
                    ".modal-close",
                    ".popup-close",
                    "[aria-label='Close']",
                    ".ant-modal-close",
                    ".el-dialog__close"
                ]
                for selector in common_popups:
                    if self.page.locator(selector).count() > 0:
                        self.page.locator(selector).first.click()
                        return
            else:
                if close_button_locator:
                    if self.find(popup_locator).is_visible():
                        self.find(close_button_locator).click()
                else:
                    # 如果没有指定关闭按钮，尝试点击弹窗外部区域
                    self.find(popup_locator).press("Escape")
        except Exception:
            # 如果关闭失败，静默处理（弹窗可能不存在）
            pass
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000):
        """
        等待页面加载状态
        
        Args:
            state: 加载状态（"load" | "domcontentloaded" | "networkidle"）
            timeout: 超时时间（毫秒）
        """
        self.page.wait_for_load_state(state, timeout=timeout)
    
    def take_screenshot(self, path: str = None, full_page: bool = True):
        """
        截图
        
        Args:
            path: 截图保存路径，如果为None则返回字节流
            full_page: 是否截取整个页面
        
        Returns:
            bytes: 如果path为None，返回截图字节流
        """
        if path:
            self.page.screenshot(path=path, full_page=full_page)
        else:
            return self.page.screenshot(full_page=full_page)
    
    def scroll_to_element(self, locator: Union[str, Tuple[str, ...]]):
        """
        滚动到指定元素
        
        Args:
            locator: 元素定位器
        """
        self.find(locator).scroll_into_view_if_needed()
    
    def wait_for_element(self, locator: Union[str, Tuple[str, ...]], 
                        state: str = "visible", timeout: int = 30000):
        """
        等待元素状态
        
        Args:
            locator: 元素定位器
            state: 元素状态（"attached" | "detached" | "visible" | "hidden"）
            timeout: 超时时间（毫秒）
        """
        self.find(locator).wait_for(state=state, timeout=timeout)
