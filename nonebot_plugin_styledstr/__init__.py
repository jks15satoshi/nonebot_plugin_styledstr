import nonebot
from nonebot import export

from . import config as conf
from .styledstr import Styledstr


driver = nonebot.get_driver()
config = conf.Config(**driver.config.dict())

export().parser = Styledstr(config)
