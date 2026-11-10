"""
环境管理器：负责读取 settings.yaml 并提供统一配置接口
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class EnvironmentManager:
    """环境管理器，负责读取配置并提供统一接口"""
    
    def __init__(self, config_file: str = None):
        """
        初始化环境管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        if config_file is None:
            # 默认配置文件路径
            current_dir = Path(__file__).parent
            config_file = current_dir / "settings.yaml"
        
        self.config_file = Path(config_file)
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        # 读取配置文件
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 获取默认环境
        self.default_env = self.config.get("default_environment", "dev")
        
        # 从环境变量获取当前环境（优先级更高）
        self.current_env = os.getenv("TEST_ENV", self.default_env)
    
    def get_browser_config(self) -> Dict[str, Any]:
        """
        获取浏览器配置
        
        Returns:
            Dict: 浏览器配置字典
        """
        return self.config.get("browser", {})
    
    def get_base_url(self, environment: str = None) -> str:
        """
        获取指定环境的 base_url
        
        Args:
            environment: 环境名称，如果为None则使用当前环境
        
        Returns:
            str: base_url
        """
        env = environment or self.current_env
        env_config = self.config.get("environments", {}).get(env, {})
        return env_config.get("base_url", "")
    
    def get_api_base_url(self, environment: str = None) -> str:
        """
        获取指定环境的 API base_url
        
        Args:
            environment: 环境名称，如果为None则使用当前环境
        
        Returns:
            str: API base_url
        """
        env = environment or self.current_env
        env_config = self.config.get("environments", {}).get(env, {})
        return env_config.get("api_base_url", "")
    
    def get_account(self, environment: str = None) -> Dict[str, str]:
        """
        获取指定环境的账号信息
        
        Args:
            environment: 环境名称，如果为None则使用当前环境
        
        Returns:
            Dict: 包含 username 和 password 的字典
        """
        env = environment or self.current_env
        env_config = self.config.get("environments", {}).get(env, {})
        return env_config.get("account", {})
    
    def get_dingtalk_config(self) -> Dict[str, Any]:
        """
        获取钉钉通知配置
        
        Returns:
            Dict: 钉钉配置字典
        """
        return self.config.get("dingtalk", {})
    
    def get_email_config(self) -> Dict[str, Any]:
        """
        获取邮件通知配置
        
        Returns:
            Dict: 邮件配置字典
        """
        return self.config.get("email", {})
    
    def get_report_config(self) -> Dict[str, Any]:
        """
        获取测试报告配置
        
        Returns:
            Dict: 报告配置字典
        """
        return self.config.get("report", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        获取日志配置
        
        Returns:
            Dict: 日志配置字典
        """
        return self.config.get("logging", {})
    
    def get_environment_config(self, environment: str = None) -> Dict[str, Any]:
        """
        获取指定环境的完整配置
        
        Args:
            environment: 环境名称，如果为None则使用当前环境
        
        Returns:
            Dict: 环境配置字典
        """
        env = environment or self.current_env
        return self.config.get("environments", {}).get(env, {})
    
    def set_environment(self, environment: str):
        """
        设置当前环境
        
        Args:
            environment: 环境名称
        """
        if environment not in self.config.get("environments", {}):
            raise ValueError(f"环境不存在: {environment}")
        self.current_env = environment
    
    def get_current_environment(self) -> str:
        """
        获取当前环境名称
        
        Returns:
            str: 当前环境名称
        """
        return self.current_env


# 全局环境管理器实例
env_manager = EnvironmentManager()
