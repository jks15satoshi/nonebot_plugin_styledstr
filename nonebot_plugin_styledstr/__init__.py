"""风格化字符串管理"""
import nonebot
from nonebot import export

from . import config as conf
from .styledstr import Styledstr


driver = nonebot.get_driver()
config = conf.Config(**driver.config.dict())

# 导出解析器对象
export().parser = Styledstr(config)
