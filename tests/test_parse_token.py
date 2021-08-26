import pytest


@pytest.mark.usefixtures('get_parser')
class TestParseToken(object):
    """测试解析字符串标签"""

    @pytest.mark.parametrize('token, expected',
                             [('token_value', 1), ('token.value', 2),
                              ('token.layer.value', 3),
                              ('token.layer.layer.value', 4),
                              ('token.layer.layer.layer.value', 5)])
    def test_parse_hierarchical_token(self, token: str, expected: int) -> None:
        """
        测试解析层级标签。

        测试预期：解析层级与预期层级相符。

        参数：
        - `token: str`：字符串标签。
        - `expected: int`：预期层级。
        """
        assert self.parser.parse(token) == f'Layer {expected}'

    @pytest.mark.parametrize(
        'token, expected',
        [('not,a,valid,token', 'is regarded as invalid or nonexistent'),
         ('token_value.layer', 'is regarded as invalid or nonexistent'),
         ('token.layer', 'is not a string')])
    @pytest.mark.usefixtures('caplog')
    def test_parse_unexpected_token(self, token: str, expected: str) -> None:
        """
        测试解析非预期的字符串标签（包括错误的字符串标签与非对应字符串资源的字
        符串标签）。

        测试预期：日志输出指定警告内容。
        """
        self.parser.parse(token)
        assert all(i for i in [token, expected] if i in self.caplog.text)

    def test_parse_token_with_multiple_values_indicated(self) -> None:
        """
        测试解析具有多个值的字符串标签。

        测试预期：随机从多个值中抽取内容输出。
        """
        result = self.parser.parse('token_with_multiple_values')
        assert result in {'value 1', 'value 2', 'value 3'}
