"""风格化字符串解析器"""
import json
import random
import re
from functools import reduce
from pathlib import Path
from typing import Any, Dict, Optional, Union

import nonebot
import yaml
from nonebot.log import logger

from . import config as conf
from . import exception


class Parser(object):

    def __init__(self, **config) -> None:
        """
        实例化解析器。

        可选参数：
        - `**config`：插件配置，覆盖 NoneBot 读取的插件配置。
        """
        init_conf = nonebot.get_driver().config.dict()
        if config:
            init_conf.update(config)

        init = conf.Config(**init_conf)

        self.__respath = init.styledstr_respath
        self.__preset = init.styledstr_preset

    def parse(self,
              token: str,
              preset: Optional[Union[str, Path]] = None,
              **placeholders) -> str:
        """
        解析字符串标签，根据风格预设配置信息获取字符串内容，并替换内容中的占位
        符（如果存在）。

        参数：
        - `token: str`：字符串标签。

        关键字参数：
        - `preset: Union[str, pathlib.Path]`：风格预设。默认为项目配置中设置的
          风格预设，未在配置中设置时为 `default`。
          - 当 `preset` 为 `str` 且 `preset` 包含预设文件后缀名时，将视为相对于
            资源目录的文件相对路径，否则将视为风格预设名称；
          - 当 `preset` 为 `pathlib.Path` 对象时，视为文件绝对路径。
        - `**placeholders`：将被替换的占位符及替换内容。

        返回：
        - `str`：根据标签获取的字符串。异常时返回空字符串。
        """
        preset = self.__preset if not preset else preset
        result = ''

        try:
            strings = self.__load_preset(preset)
            result = self.__token_parse(token, strings)
        except (exception.PresetFileError, exception.TokenError) as err:
            err.log()
        else:
            if placeholders:
                result = self.__replace_placeholders(result, **placeholders)
            logger.debug(f'Token "{token}" parsed as expected.')

        return result

    def __load_preset(self, preset: Union[str, Path]) -> Dict[str, Any]:
        """
        加载风格预设文件内容。

        参数：
        - `preset: Union[str, pathlib.Path]`：风格预设。

        异常：
        - `exception.ResourcePathError`：资源目录未有效设置。
        - `exception.PresetFileError`：指定预设名称错误或预设文件不存在。

        返回:
        - `Dict[str, Any]`：风格预设内容。
        """
        valid_format = r'\.(?:json|ya?ml)'
        preset_file = None

        is_file_path = re.search(valid_format, str(preset))

        # preset 为风格预设名称
        if isinstance(preset, str) and not is_file_path:
            valid_file = ''.join([preset, valid_format])
            files = [
                file for file in self.__respath.iterdir()
                if re.match(valid_file, file.name, re.IGNORECASE)
            ]

            if not files:
                raise exception.PresetFileError(preset, self.__respath)

            files.sort()
            preset_file = files[0]
        # preset 为风格预设文件的相对或绝对路径
        else:
            if isinstance(preset, Path):
                preset_file = preset
            else:
                preset_file = (Path(preset) if Path(preset).is_file() else
                               self.__respath / preset)

            if not preset_file.exists():
                message = (f'Preset file {preset_file.absolute()} does not '
                           'exist.')
                raise exception.PresetFileError(message=message)

        loaded = {}
        with preset_file.open() as f:
            if re.match(r'\.ya?ml', preset_file.suffix):
                loaded = yaml.safe_load(f)
            else:
                loaded = json.load(f)

        logger.info(f'Preset file {preset_file.name} loaded.')
        return loaded

    @staticmethod
    def __replace_placeholders(contents: str, /, **placeholders) -> str:
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
        blacklist = {'contents', 'preset', 'token'}

        items = {i for i, _ in placeholders.items()}
        replaced_items = set()

        split_str = re.split(placeholder, contents)

        for i, item in enumerate(split_str):
            if (re.match(placeholder, item)
                    and (val := item[1:-1].lower()) not in blacklist):
                replaced = placeholders.get(val)
                if replaced:
                    split_str[i] = str(replaced)
                    replaced_items.add(str(val))
                else:
                    split_str[i] = item

        if (invalid := items - replaced_items):
            logger.warning('The following placeholders are regarded as '
                           'invalid or nonexistent and skipped replacing: '
                           f'{invalid}')
        return ''.join(split_str)

    @staticmethod
    def __token_parse(token: str, preset_contents: Dict[str, Any]) -> str:
        """
        解析字符串标签。

        参数：
        - `token: str`：字符串标签。
        - `preset_contents: Dict[str, Any]`：风格预设内容。

        异常：
        - `exception.TokenError`：字符串标签不存在于风格预设内容中，或其对应内
          容不是数值、布尔值、字符串或列表。

        返回：
        - `str`：标签所指示的字符串内容。特别地，当 `preset_contents` 中字符串
          标签所对应的内容为列表时，则从中随机抽取值返回。
        """
        try:
            result = reduce(lambda key, val: key[val], token.split('.'),
                            preset_contents)
        except (KeyError, TypeError):
            raise exception.TokenError(token)
        else:
            if isinstance(result, list):
                return str(random.choice(result))
            if isinstance(result, (str, int, float, bool)):
                return str(result)

            message = (
                f'The value of the token "{token}" is not a numeric, boolean, '
                'string or list.')
            raise exception.TokenError(message=message)
