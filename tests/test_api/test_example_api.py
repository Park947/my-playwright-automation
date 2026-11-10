"""
API 自动化测试用例示例
"""
import pytest
import requests
from config.environments import env_manager
from utils.helper_methods import get_logger


logger = get_logger()


@pytest.mark.api
@pytest.mark.functional
@pytest.mark.parametrize("case", [
    {"id": 1, "expected_status": 200},
    {"id": 2, "expected_status": 200},
    {"id": 999, "expected_status": 404},  # 不存在的ID
])
def test_example_api(case):
    """
    参数化 API 测试示例
    
    测试不同ID的API响应
    """
    api_base_url = env_manager.get_api_base_url()
    
    # 构建请求URL（根据实际API调整）
    url = f"{api_base_url}/api/example/{case['id']}"
    
    # 发送请求
    logger.info(f"请求URL: {url}")
    response = requests.get(url, timeout=10)
    
    # 断言状态码
    assert response.status_code == case["expected_status"], \
        f"期望状态码 {case['expected_status']}，实际 {response.status_code}"
    
    # 如果成功，验证响应体
    if response.status_code == 200:
        body = response.json()
        assert "data" in body or "result" in body, "响应应包含 data 或 result 字段"
        logger.info(f"API响应: {body}")


@pytest.mark.api
@pytest.mark.smoke
def test_api_health_check():
    """
    API 健康检查测试
    
    验证API服务是否可用
    """
    api_base_url = env_manager.get_api_base_url()
    health_url = f"{api_base_url}/health"
    
    try:
        response = requests.get(health_url, timeout=5)
        assert response.status_code == 200, f"健康检查失败，状态码: {response.status_code}"
        logger.info("API健康检查通过")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"API健康检查失败: {e}")


@pytest.mark.api
@pytest.mark.functional
def test_api_with_authentication():
    """
    需要认证的API测试示例
    
    演示如何发送带认证信息的请求
    """
    api_base_url = env_manager.get_api_base_url()
    account = env_manager.get_account()
    
    # 构建请求（根据实际API调整）
    url = f"{api_base_url}/api/protected"
    
    # 方式1：使用 Basic Auth
    # response = requests.get(url, auth=(account["username"], account["password"]))
    
    # 方式2：使用 Token（需要先获取token）
    # token = get_auth_token()  # 需要实现获取token的方法
    # headers = {"Authorization": f"Bearer {token}"}
    # response = requests.get(url, headers=headers)
    
    # 示例：简单的GET请求
    response = requests.get(url, timeout=10)
    
    # 根据实际业务调整断言
    assert response.status_code in [200, 401], \
        f"API响应状态码异常: {response.status_code}"
