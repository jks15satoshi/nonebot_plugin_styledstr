"""插件异常"""
from pathlib import Path
from typing import Optional

from nonebot.log import logger


class StyledstrError(Exception):
    """
    异常基类。

    属性：
    - `message: str`：日志信息。
    """

    def __init__(self, message: str) -> None:
        """
        异常初始化。

        参数：
        - `message: str`：日志信息。
        """
        self.message = message

    def log(self) -> None:
        """格式化日志输出。"""
        logger.opt(colors=True).error(f'<R><b>{self.message}</b></R>')


class PresetFileError(StyledstrError):
    """
    异常初始化。

    提供两种异常消息格式：
    - 默认格式：提供参数 `preset` 与 `respath`，此时日志输出为 `respath` 下不存
      在 `preset` 风格预设；
    - 自定义格式：提供参数 `message`，此时日志输出消息内容自定义。

    关键字参数：
    - `preset: Optional[str]`：预设名称。
    - `respath: Optional[pathlib.Path]`：资源目录路径。
    - `message: str`：日志信息。默认为空字符串。
    """

    def __init__(self,
                 /,
                 preset: Optional[str] = None,
                 respath: Optional[Path] = None,
                 *,
                 message: str = '') -> None:
        if message:
            msg = message
        elif preset and respath:
            msg = (f'Cannot find any valid file for preset "{preset}" from '
                   f'the resource path {respath.absolute()}.')
        else:
            msg = 'Cannot find any valid file for the indicated preset.'

        super().__init__(msg)


class TokenError(StyledstrError):
    """
    字符串标签异常。

    提供两种异常消息格式：
    - 默认格式：提供参数 `token`，此时日志输出为 `token` 参数解析异常；
    - 自定义格式：提供参数 `message`，此时日志输出消息内容自定义。

    关键字参数：
    - `token: str`：字符串标签；
    - `message: str`：日志信息。默认为空字符串。
    """

    def __init__(self, /, token: str = '', *, message: str = '') -> None:
        super().__init__(
            f'Token "{token}" is regarded as invalid or '
            'nonexistent and skipped parsing.' if not message else message)
