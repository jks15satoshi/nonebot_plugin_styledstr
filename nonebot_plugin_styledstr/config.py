"""插件配置"""
from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    styledstr_respath: Path = Path()
    styledstr_preset: str = 'default'

    class Config:
        extra = 'ignore'
