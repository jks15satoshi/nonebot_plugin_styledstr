from pathlib import Path
from typing import Any, Dict

import pytest

cases_custom_config = [
    ({
        'styledstr_preset': 'alter'
    }, 'assets/alter.yaml'),
    ({
        'styledstr_respath': (Path(__file__).parent / 'assets' / 'test_import')
    }, 'assets/test_import/test.yaml'),
    ({
        'styledstr_respath':
            (Path(__file__).parent / 'assets' / 'test_import'),
        'styledstr_preset': 'alter'
    }, 'assets/test_import/alter.yaml')
]


@pytest.mark.usefixtures('setup')
class TestExport(object):
    """测试通过 require 获取或创建解析器对象"""

    def test_default_export(self) -> None:
        """
        测试以默认配置获取解析器对象。

        测试预期：正常解析字符串标签。
        """
        from nonebot import require

        parser = require('nonebot_plugin_styledstr').init()
        assert parser.parse('test.status') == 'success'

    @pytest.mark.parametrize('config, expected_dirname', cases_custom_config)
    def test_export_with_custom_attr_config(self, config: Dict[str, Any],
                                            expected_dirname: str) -> None:
        """
        测试自定义配置（参数）创建解析器对象。

        测试预期：通过将配置项以参数形式传入创建解析器对象，并加载配置所指定的
        预设文件。

        参数：
        - `config: Dict[str, Any]`：自定义类型。
        - `expected_dirname: str`：预期加载文件。
        """
        from nonebot import require

        parser = require('nonebot_plugin_styledstr').init(config)
        assert parser.parse('test.dirname') == expected_dirname

    @pytest.mark.parametrize('config, expected_dirname', cases_custom_config)
    def test_export_with_custom_nonebot_config(self, config: Dict[str, Any],
                                               expected_dirname: str) -> None:
        """
        测试自定义配置（`nonebot.config.Config` 对象）创建解析器对象。

        测试预期：通过传入 `nonebot.config.Config` 对象创建解析器对象，并加载配
        置所指定的预设文件。

        参数：
        - `config: Dict[str, Any]`：自定义类型。
        - `expected_dirname: str`：预期加载文件。
        """
        from nonebot import config as nb_conf
        from nonebot import require

        conf = nb_conf.Config(**config)

        parser = require('nonebot_plugin_styledstr').init(conf)
        assert parser.parse('test.dirname') == expected_dirname
