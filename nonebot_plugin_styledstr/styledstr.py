"""风格化字符串解析器"""
import json
import re
from functools import reduce
from typing import Any

import yaml
from nonebot.log import logger

from . import config as conf
from . import exception


class Styledstr(object):
    def __init__(self, config: conf.Config) -> None:
        """
        实例化解析器。

        参数：
        - `config: config.Config`：插件配置。
        """
        self.res_path = config.styledstr_respath
        self.preset = config.styledstr_preset

    def parse(self, token: str, preset=None, **placeholders) -> str:
        """
        解析字符串标签，根据风格预设配置信息获取字符串内容，并替换内容中的占位
        符（如果存在）。

        参数：
        - `token: str`：字符串标签。

        关键字参数：
        - `preset: str`：风格预设。默认为项目配置中设置的风格预设，未在配置中设
        置时为 `default`。
        - `**placeholders`：将被替换的占位符及替换内容。

        返回：
        - `str`：根据标签获取的字符串。
        """
        preset = self.preset if not preset else preset
        result = ''

        try:
            strings = self.__load_preset(preset)
            result = self.__token_parse(token, strings)
        except (exception.PresetFileError, exception.ResourcePathError,
                exception.TokenError) as err:
            err.log()
        else:
            if placeholders:
                result = self.__replace_placeholders(result, **placeholders)
            logger.debug(f'Token "{token}" parsed as expected.')

        return result

    def __load_preset(self, preset: str) -> dict[str, Any]:
        """
        加载风格预设文件内容。

        参数：
        - `preset: str`：风格预设名称。

        异常：
        - `exception.ResourcePathError`：资源目录未有效设置。
        - `exception.PresetFileError`：指定预设名称错误或预设文件不存在。

        返回:
        - `dict[str, Any]`：风格预设内容。
        """
        if not (path := self.res_path):
            raise exception.ResourcePathError()
        else:
            valid_file = ''.join([preset, r'\.(?:json|ya?ml)'])

            preset_file = None
            for file in path.iterdir():
                if re.match(valid_file, file.name, re.IGNORECASE):
                    preset_file = file
                    break

            if not preset_file:
                raise exception.PresetFileError(preset)
            else:
                loaded = {}
                with preset_file.open() as f:
                    if re.match(r'\.ya?ml', preset_file.suffix):
                        loaded = yaml.safe_load(f)
                    else:
                        loaded = json.load(f)

                logger.info(f'Preset file {preset_file.name} loaded.')
                return loaded

    @staticmethod
    def __replace_placeholders(contents: str, **placeholders) -> str:
        """
        替换字符串中的占位符为指定内容。

        参数：
        - `contents: str`：包含占位符的字符串内容。

        关键字参数：
        - `**placeholders`：将被替换的占位符及替换内容。

        返回：
        - `str`：处理后的字符串。
        """
        placeholder = r'(\$[a-zA-Z]\w{0,23}\$)'

        split_str = re.split(placeholder, contents)

        for i, item in enumerate(split_str):
            if re.match(placeholder, item):
                split_str[i] = placeholders.get(item[1:-1].lower())

        return ''.join(split_str)

    @staticmethod
    def __token_parse(token: str, preset_contents: dict[str, Any]) -> str:
        """
        解析字符串标签。

        参数：
        - `token: str`：字符串标签。
        - `preset_contents: dict[str, Any]`：风格预设内容。

        异常：
        - `exception.TokenError`：字符串标签不存在于风格预设内容中。

        返回：
        - `str`：标签所指示的字符串内容。
        """
        try:
            result = reduce(lambda key, val: key[val], token.split('.'),
                            preset_contents)
        except KeyError:
            raise exception.TokenError(token)
        else:
            return result
