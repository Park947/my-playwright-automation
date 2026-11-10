"""
示例页面对象（用于演示框架用法）
"""
from Common.baseView import BasePage
from typing import Union, Tuple


class ExamplePageLocators:
    """示例页面定位器"""
    MENU_BUTTON = ("role", "button", "Menu")
    SEARCH_INPUT = "#search-input"
    SEARCH_RESULT = ".search-result-item"
    SEARCH_BUTTON = ("role", "button", "Search")


class ExamplePage(BasePage):
    """示例页面对象"""
    
    def open_menu(self):
        """打开菜单"""
        self.find(ExamplePageLocators.MENU_BUTTON).click()
        self.page.wait_for_timeout(500)  # 等待菜单动画
    
    def search(self, keyword: str):
        """
        执行搜索操作
        
        Args:
            keyword: 搜索关键词
        """
        # 输入搜索关键词
        self.find(ExamplePageLocators.SEARCH_INPUT).fill(keyword)
        
        # 按 Enter 键或点击搜索按钮
        self.find(ExamplePageLocators.SEARCH_INPUT).press("Enter")
        # 或者：self.find(ExamplePageLocators.SEARCH_BUTTON).click()
        
        # 等待搜索结果加载
        self.page.wait_for_load_state("networkidle")
    
    def get_first_result_text(self) -> str:
        """
        获取第一个搜索结果的文本
        
        Returns:
            str: 第一个搜索结果的文本内容
        """
        return self.find(ExamplePageLocators.SEARCH_RESULT).first.text_content().strip()
    
    def get_all_results(self) -> list:
        """
        获取所有搜索结果的文本列表
        
        Returns:
            list: 所有搜索结果的文本列表
        """
        results = []
        count = self.find(ExamplePageLocators.SEARCH_RESULT).count()
        for i in range(count):
            text = self.find(ExamplePageLocators.SEARCH_RESULT).nth(i).text_content().strip()
            results.append(text)
        return results
