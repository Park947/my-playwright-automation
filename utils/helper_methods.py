"""
日志、通用工具函数
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from config.environments import env_manager


class Logger:
    """统一的日志封装类"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = "test") -> logging.Logger:
        """
        获取日志记录器（单例模式）
        
        Args:
            name: 日志记录器名称
        
        Returns:
            logging.Logger: 日志记录器实例
        """
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            
            # 避免重复添加处理器
            if not logger.handlers:
                # 获取日志配置
                log_config = env_manager.get_logging_config()
                log_level = getattr(logging, log_config.get("level", "INFO"))
                log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                
                # 控制台处理器
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_level)
                console_formatter = logging.Formatter(log_format)
                console_handler.setFormatter(console_formatter)
                logger.addHandler(console_handler)
                
                # 文件处理器
                log_dir = Path(log_config.get("log_dir", "tests/logs"))
                log_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_file_template = log_config.get("log_file", "test_{timestamp}.log")
                log_file = log_file_template.format(timestamp=timestamp)
                log_path = log_dir / log_file
                
                file_handler = logging.FileHandler(log_path, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别
                file_formatter = logging.Formatter(log_format)
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            
            cls._loggers[name] = logger
        
        return cls._loggers[name]


def get_logger(name: str = "test") -> logging.Logger:
    """
    获取日志记录器的便捷函数
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    return Logger.get_logger(name)


def wait_for_condition(condition_func, timeout: int = 30, interval: float = 0.5, 
                       error_message: str = "条件未满足"):
    """
    等待条件满足
    
    Args:
        condition_func: 条件函数，返回 True 表示条件满足
        timeout: 超时时间（秒）
        interval: 检查间隔（秒）
        error_message: 超时时的错误消息
    
    Raises:
        TimeoutError: 超时时抛出异常
    """
    import time
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if condition_func():
            return
        time.sleep(interval)
    
    raise TimeoutError(f"{error_message} (超时: {timeout}秒)")


def retry_on_failure(max_attempts: int = 3, delay: float = 1.0, 
                     exceptions: tuple = (Exception,)):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大尝试次数
        delay: 重试延迟（秒）
        exceptions: 需要重试的异常类型
    
    Example:
        @retry_on_failure(max_attempts=3, delay=1.0)
        def my_function():
            # 可能失败的代码
            pass
    """
    def decorator(func):
        import time
        import functools
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger = get_logger()
                        logger.warning(f"{func.__name__} 第 {attempt} 次尝试失败: {e}，{delay}秒后重试...")
                        time.sleep(delay)
                    else:
                        logger = get_logger()
                        logger.error(f"{func.__name__} 重试 {max_attempts} 次后仍失败")
            
            raise last_exception
        return wrapper
    return decorator


def format_duration(seconds: float) -> str:
    """
    格式化时长
    
    Args:
        seconds: 秒数
    
    Returns:
        str: 格式化后的时长字符串，如 "1小时30分15秒"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}小时")
    if minutes > 0:
        parts.append(f"{minutes}分")
    if secs > 0:
        parts.append(f"{secs}秒")
    
    return "".join(parts) if parts else "0秒"


def generate_test_data(data_type: str = "string", length: int = 10) -> str:
    """
    生成测试数据
    
    Args:
        data_type: 数据类型（"string" | "number" | "email" | "phone"）
        length: 数据长度
    
    Returns:
        str: 生成的测试数据
    """
    import random
    import string
    
    if data_type == "string":
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    elif data_type == "number":
        return ''.join(random.choices(string.digits, k=length))
    elif data_type == "email":
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{username}@example.com"
    elif data_type == "phone":
        return f"1{''.join(random.choices(string.digits, k=10))}"
    else:
        raise ValueError(f"不支持的数据类型: {data_type}")
