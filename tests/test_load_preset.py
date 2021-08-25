from pathlib import Path
from typing import List, Union

import pytest

assets_path = Path(__file__).parent / 'assets'


class TestLoadPreset(object):
    """测试加载预设文件"""

    @pytest.mark.parametrize('path, expected', [
        (assets_path / 'test_load_same_preset' / 'load_json_yaml', '.json'),
        (assets_path / 'test_load_same_preset' / 'load_json_yml', '.json'),
        (assets_path / 'test_load_same_preset' / 'load_yaml_yml', '.yaml'),
        (assets_path / 'test_load_same_preset' / 'load_json_yaml_yml', '.json')
    ])
    @pytest.mark.usefixtures('setup')
    def test_load_preset_from_multiple_same_files(self, path: Path,
                                                  expected: str) -> None:
        """
        测试从多个被视为同一预设的文件中读取预设文件。

        测试预期：按照 `.json` > `.yaml` > `.yml` 的优先级读取。

        参数：
        - `path: pathlib.Path`：测试路径。
        - `expected: str`：预期读取文件的后缀名。
        """
        from nonebot import require

        config = {'styledstr_respath': path, 'styledstr_preset': 'load'}
        parser = require('nonebot_plugin_styledstr').init(config)

        assert parser.parse('test.dirname').endswith(expected)

    @pytest.mark.parametrize(
        'preset, expected',
        [('alter', 'assets/alter.yaml'), ('alter.yml', 'assets/alter.yml'),
         ('test_import/test.yaml', 'assets/test_import/test.yaml'),
         (assets_path / 'test_import' / 'alter.yaml',
          'assets/test_import/alter.yaml')])
    @pytest.mark.usefixtures('get_parser')
    def test_load_preset_while_parsing_token(self, preset: Union[str, Path],
                                             expected: str) -> None:
        """
        测试以自定义风格预设获取内容。

        测试预期：读取指定的风格预设文件。

        参数：
        - `preset: Union[str, pathlib.Path]`：风格预设。
        - `expected: str`：预期读取的文件。
        """
        assert self.parser.parse('test.dirname', preset=preset) == expected

    @pytest.mark.parametrize(
        'preset, expected',
        [('default', ['Cannot find', 'preset default']),
         ('alter.json', ['Preset file', 'assets/alter.json']),
         ('test_import/test.json',
          ['Preset file', 'assets/test_import/test.json']),
         (assets_path / 'test_import' / 'alter.json',
          ['Perset file', 'assets/test_import/alter.json'])])
    @pytest.mark.usefixtures('get_parser', 'caplog')
    def test_logging_while_parsing_token(self, preset: Union[str, Path],
                                         expected: List[str]) -> None:
        """
        测试日志输出。

        测试预期：日志输出包含 `expected` 中所有内容。

        参数：
        - `preset: Union[str, pathlib.Path]`：风格预设。
        - `expected: str`：预期日志出现文本内容。
        """
        self.parser.parse('test.dirname', preset=preset)
        assert all(i for i in expected if i in self.caplog.text)
