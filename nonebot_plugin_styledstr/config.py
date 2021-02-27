from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    respath: Path = Path()
    preset: str = 'default'

    class Config:
        extra = 'ignore'
