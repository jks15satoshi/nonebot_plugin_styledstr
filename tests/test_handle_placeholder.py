from typing import Any, Dict

import pytest

cases_replace_placeholder = [('placeholder.testchamber_text', {
    'text': 'pass'
}), ('placeholder.testchamber_capital', {
    'text': 'pass'
}), ('placeholder.testchamber_underscore', {
    'underscored_text': 'pass'
}), ('placeholder.testchamber_number', {
    'test4science': 'pass'
}), ('placeholder.testchamber_edgecase', {
    'complicated__placeholder': 'pass'
})]

cases_handle_invalid_placeholder = [
    ('placeholder.testchamber_text', {
        'nonexistence': 'failed'
    }), ('placeholder.testchamber_text', {
        'Text': 'failed'
    }),
    ('placeholder.testchamber_invalid.underscore_prefix', {
        '__main__': 'failed'
    }),
    ('placeholder.testchamber_invalid.number_prefix', {
        '1placeholder': 'failed'
    }),
    ('placeholder.testchamber_invalid.out_of_length', {
        'a_complicated_placeholder': 'failed'
    })
]

cases_handle_multiple_placeholders = [
    ('placeholder.testchamber_multiple.normal', {
        'subject': 'The quick brown fox',
        'action': 'jumps over',
        'object': 'the lazy dog'
    }, 'The quick brown fox jumps over the lazy dog.'),
    ('placeholder.testchamber_multiple.with_dollar', {
        'value': 1.27,
        'date': 'Jan 1, 2021',
        'provider': 'Morningstar'
    }, ('US$ 1.00 approx. equals CA$ 1.27 (data provided by Morningstar on '
        'Jan 1, 2021).')),
    ('placeholder.testchamber_multiple.with_invalid', {
        '_invalid_placeholder': 'invalid placeholder',
        'normal_placeholder': 'normal one'
    }, ('The $_invalid_placeholder$ will be ignored, and the normal one will '
        'not.')),
    ('placeholder.testchamber_multiple.with_duplicate', {
        'can': 'can',
        'a_can': 'a can',
        'canner': 'canner'
    }, 'Can you can a can as a canner can can a can?')
]


@pytest.mark.usefixtures('get_parser')
class TestHandlePlaceholder(object):
    """测试占位符处理"""

    @pytest.mark.parametrize('token, placeholder', cases_replace_placeholder)
    def test_replace_placeholder(self, token: str,
                                 placeholder: Dict[str, Any]) -> None:
        """
        测试占位符内容替换。

        测试预期：占位符被替换为字符串 `pass`。

        参数：
        - `token: str`：字符串标签。
        - `placeholder: Dict[str, Any]`：占位符名称。
        """
        text = self.parser.parse(token, **placeholder)
        assert text == 'pass'

    @pytest.mark.parametrize('token, placeholder',
                             cases_handle_invalid_placeholder)
    def test_handle_invalid_placeholder(self, token: str,
                                        placeholder: Dict[str, Any]) -> None:
        """
        测试无效占位符处理。
        无效占位符包括传入非小写的占位符参数以及使用不存在或无效的占位符名称。

        测试预期：无内容变动。

        参数：
        - `token: str`：字符串标签。
        - `placeholder: Dict[str, Any]`：占位符名称。
        """
        text = self.parser.parse(token, **placeholder)
        assert text == self.parser.parse(token)

    # 测试多个占位符处理（可能出现非预期的占位符）。
    # 预期结果：符合测试样例中 expected 的内容。
    @pytest.mark.parametrize('token, placeholders, expected',
                             cases_handle_multiple_placeholders)
    def test_handle_multiple_placeholders(self, token: str,
                                          placeholders: Dict[str, Any],
                                          expected: str) -> None:
        """
        测试多个占位符处理。

        测试预期：处理后文本与参数 `expected` 值匹配。

        参数：
        - `token: str`：字符串标签。
        - `placeholder: Dict[str, Any]`：占位符名称。
        - `expected: str`：测试预期结果。
        """
        text = self.parser.parse(token, **placeholders)
        assert text == expected

    def test_handle_placeholder_with_random_value(self) -> None:
        """
        测试随机抽取内容的占位符处理。

        测试预期：`$test$` 占位符替换为 `TEXT`。
        """
        text = self.parser.parse('placeholder.testchamber_with_random_values',
                                 test='TEXT')
        assert text in {'TEXT 1', 'TEXT 2', '$text$ 3'}

    def test_logging_while_handling_placeholders(self, caplog) -> None:
        """
        测试处理占位符时的日志输出。

        参数：
        - `caplog`：捕捉日志输出固件。
        """
        placeholders = {
            'test': 'RELAID WORDS: ',
            'prepare': 'Prepare ',
            '4unforeseen': 'for unforeseen ',
            '_consequences': 'consequences.'
        }
        self.parser.parse('placeholder.testchamber_logcat', **placeholders)

        warning_text = ('The following placeholders are regarded as invalid '
                        'or nonexistent and skipped replacing')
        invalid = ['test', '4unforeseen', '_consequences']

        assert warning_text in caplog.text
        assert any(i in caplog.text for i in invalid)
