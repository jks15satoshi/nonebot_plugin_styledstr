"""插件配置"""
from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    """
    插件配置类。

    继承自 pydantic.BaseSettings。

    属性：
    - `styledstr_respath: pathlib.Path`：资源目录路径，默认为当前工作目录；
    - `styledstr_preset: str`：预设名称，默认为 `default`。
    """

    styledstr_respath: Path = Path()
    styledstr_preset: str = 'default'

    class Config(object):
        """Pydantic model config"""

        extra = 'ignore'
