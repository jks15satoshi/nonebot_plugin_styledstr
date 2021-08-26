"""风格化字符串管理"""
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Dict, Union

import toml
from nonebot import config as nb_conf
from nonebot import export
from nonebot.log import logger

from .styledstr import Parser

# 日志输出版本信息
try:
    __version__ = version('nonebot_plugin_styledstr')
except PackageNotFoundError:
    with (Path(__file__).parents[1] / 'pyproject.toml').open() as file:
        __version__ = toml.load(file)['tool']['poetry']['version']

logger.info(f'Plugin loaded: nonebot_plugin_styledstr v{__version__}')


# 导出创建解析器对象方法
@export()
def init(config: Union[nb_conf.Config, Dict[str, Any], None] = None) -> Parser:
    """
    创建解析器对象。

    可选参数：
    - `config: Union[nonebot.config.Config, dict[str, Any], None]`：插件配置。

    返回：
    - `styledstr.Styledstr`：解析器对象。
    """
    if not config:
        parser = Parser()
    elif isinstance(config, dict):
        parser = Parser(**config)
    else:
        parser = Parser(**config.dict())

    return parser
