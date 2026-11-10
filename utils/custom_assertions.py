"""
自定义断言：提供更友好的断言方法和错误信息
"""
from typing import Any, List, Dict
from utils.helper_methods import get_logger


logger = get_logger()


def assert_contains(actual: str, expected: str, message: str = None):
    """
    断言字符串包含
    
    Args:
        actual: 实际值
        expected: 期望包含的字符串
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if expected not in actual:
        error_msg = message or f"期望 '{actual}' 包含 '{expected}'，但实际不包含"
        logger.error(error_msg)
        raise AssertionError(error_msg)


def assert_not_contains(actual: str, expected: str, message: str = None):
    """
    断言字符串不包含
    
    Args:
        actual: 实际值
        expected: 期望不包含的字符串
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if expected in actual:
        error_msg = message or f"期望 '{actual}' 不包含 '{expected}'，但实际包含"
        logger.error(error_msg)
        raise AssertionError(error_msg)


def assert_equal(actual: Any, expected: Any, message: str = None):
    """
    断言相等（带日志）
    
    Args:
        actual: 实际值
        expected: 期望值
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if actual != expected:
        error_msg = message or f"期望值: {expected}，实际值: {actual}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug(f"断言通过: {actual} == {expected}")


def assert_not_equal(actual: Any, expected: Any, message: str = None):
    """
    断言不相等（带日志）
    
    Args:
        actual: 实际值
        expected: 期望值
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if actual == expected:
        error_msg = message or f"期望值不等于 {expected}，但实际值: {actual}"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug(f"断言通过: {actual} != {expected}")


def assert_true(condition: bool, message: str = None):
    """
    断言为真（带日志）
    
    Args:
        condition: 条件
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if not condition:
        error_msg = message or "期望条件为真，但实际为假"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug("断言通过: 条件为真")


def assert_false(condition: bool, message: str = None):
    """
    断言为假（带日志）
    
    Args:
        condition: 条件
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if condition:
        error_msg = message or "期望条件为假，但实际为真"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug("断言通过: 条件为假")


def assert_in(item: Any, container: List | Dict | str, message: str = None):
    """
    断言元素在容器中
    
    Args:
        item: 要查找的元素
        container: 容器（列表、字典或字符串）
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if item not in container:
        error_msg = message or f"期望 {item} 在 {container} 中，但实际不在"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug(f"断言通过: {item} 在容器中")


def assert_not_in(item: Any, container: List | Dict | str, message: str = None):
    """
    断言元素不在容器中
    
    Args:
        item: 要查找的元素
        container: 容器（列表、字典或字符串）
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if item in container:
        error_msg = message or f"期望 {item} 不在 {container} 中，但实际在"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug(f"断言通过: {item} 不在容器中")


def assert_greater_than(actual: float | int, expected: float | int, message: str = None):
    """
    断言大于
    
    Args:
        actual: 实际值
        expected: 期望值
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if actual <= expected:
        error_msg = message or f"期望 {actual} > {expected}，但实际不满足"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug(f"断言通过: {actual} > {expected}")


def assert_less_than(actual: float | int, expected: float | int, message: str = None):
    """
    断言小于
    
    Args:
        actual: 实际值
        expected: 期望值
        message: 自定义错误消息
    
    Raises:
        AssertionError: 断言失败时抛出
    """
    if actual >= expected:
        error_msg = message or f"期望 {actual} < {expected}，但实际不满足"
        logger.error(error_msg)
        raise AssertionError(error_msg)
    logger.debug(f"断言通过: {actual} < {expected}")
