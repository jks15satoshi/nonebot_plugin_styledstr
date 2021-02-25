from pathlib import Path
from typing import Union

from pydantic import BaseSettings


class Config(BaseSettings):
    styledstr_respath: Union[Path, str] = Path()
    styledstr_preset: str = 'default'

    class Config:
        extra = 'ignore'
