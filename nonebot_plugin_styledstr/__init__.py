"""风格化字符串管理"""
from importlib.metadata import version
from typing import Any, Dict, Union

from nonebot import config as nb_conf
from nonebot import export
from nonebot.log import logger

from .styledstr import Parser

# 获取与日志输出版本信息
logger.info('Plugin loaded: nonebot_plugin_styledstr '
            f'v{version("nonebot_plugin_styledstr")}')


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
