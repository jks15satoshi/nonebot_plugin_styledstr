"""风格化字符串管理"""
from typing import Any, Union

from nonebot import config as nb_conf
from nonebot import export

from .styledstr import Parser


# 导出默认解析器对象
export().parser = Parser()


# 导出创建解析器对象方法
@export()
def init(config: Union[nb_conf.Config, dict[str, Any]]) -> Parser:
    """
    创建解析器对象。

    参数：
    - `config: Union[nonebot.config.Config, dict[str, Any]]`：插件配置。

    返回：
    - `styledstr.Styledstr`：解析器对象。
    """
    if isinstance(config, dict):
        parser = Parser(**config)
    else:
        parser = Parser(**config.dict())

    return parser
