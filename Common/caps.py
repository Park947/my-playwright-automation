"""
本地调试的浏览器启动封装（可选）
用于本地开发调试时快速启动浏览器
"""
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional, Dict, Any


def launch_browser(
    browser_type: str = "chromium",
    headless: bool = False,
    slow_mo: int = 0,
    viewport: Optional[Dict[str, int]] = None,
    **kwargs
) -> tuple[Browser, BrowserContext, Page]:
    """
    启动浏览器并返回 browser, context, page 实例
    
    Args:
        browser_type: 浏览器类型（"chromium" | "firefox" | "webkit"）
        headless: 是否无头模式
        slow_mo: 操作延迟（毫秒），用于调试
        viewport: 视口大小，如 {"width": 1920, "height": 1080}
        **kwargs: 其他浏览器启动参数
    
    Returns:
        tuple: (browser, context, page) 实例
    
    Example:
        browser, context, page = launch_browser(headless=False, slow_mo=500)
        page.goto("https://example.com")
        # ... 执行操作 ...
        browser.close()
    """
    playwright = sync_playwright().start()
    
    # 选择浏览器类型
    if browser_type == "chromium":
        browser = playwright.chromium.launch(headless=headless, slow_mo=slow_mo, **kwargs)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(headless=headless, slow_mo=slow_mo, **kwargs)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(headless=headless, slow_mo=slow_mo, **kwargs)
    else:
        raise ValueError(f"不支持的浏览器类型: {browser_type}")
    
    # 创建上下文
    context_options = {}
    if viewport:
        context_options["viewport"] = viewport
    else:
        context_options["viewport"] = {"width": 1920, "height": 1080}
    
    context = browser.new_context(**context_options)
    
    # 创建页面
    page = context.new_page()
    
    return browser, context, page


if __name__ == "__main__":
    # 本地调试示例
    browser, context, page = launch_browser(headless=False, slow_mo=500)
    try:
        page.goto("https://example.com")
        print(f"页面标题: {page.title()}")
        input("按 Enter 键关闭浏览器...")
    finally:
        browser.close()
