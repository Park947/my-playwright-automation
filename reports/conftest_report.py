"""
报告相关配置和辅助函数
"""
import allure
from pathlib import Path
from config.environments import env_manager


def attach_screenshot(page, name: str = "截图"):
    """
    附加截图到 Allure 报告
    
    Args:
        page: Playwright Page 对象
        name: 截图名称
    """
    try:
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"截图失败: {e}")


def attach_text(text: str, name: str = "文本内容"):
    """
    附加文本到 Allure 报告
    
    Args:
        text: 文本内容
        name: 附件名称
    """
    allure.attach(
        text,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )


def attach_json(data: dict, name: str = "JSON数据"):
    """
    附加 JSON 数据到 Allure 报告
    
    Args:
        data: JSON 数据（字典）
        name: 附件名称
    """
    import json
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    allure.attach(
        json_str,
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


def set_allure_environment():
    """
    设置 Allure 环境信息
    """
    env_config = env_manager.get_environment_config()
    browser_config = env_manager.get_browser_config()
    
    environment_info = {
        "Environment": env_manager.get_current_environment(),
        "Base URL": env_manager.get_base_url(),
        "Browser": browser_config.get("type", "chromium"),
        "Headless": str(browser_config.get("headless", True)),
        "Viewport": f"{browser_config.get('viewport', {}).get('width', 1920)}x{browser_config.get('viewport', {}).get('height', 1080)}"
    }
    
    # 生成环境文件
    report_config = env_manager.get_report_config()
    allure_results_dir = Path(report_config.get("allure_results_dir", "tests/reports/allure-results"))
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    env_file = allure_results_dir / "environment.properties"
    with open(env_file, 'w', encoding='utf-8') as f:
        for key, value in environment_info.items():
            f.write(f"{key}={value}\n")
