"""工具模块"""
import warnings
from functools import wraps
from typing import Any, Callable


def deprecated(message: str) -> Callable[..., Callable[..., Any]]:
    """
    弃用警告装饰器。

    参数：
    - `message: str`：警告信息。

    返回：
    - `Callable[..., Callable[..., Any]]`：警告装饰器。
    """

    def _deprecated(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            warnings.warn(message, DeprecationWarning)
            return result

        return wrapper

    return _deprecated
