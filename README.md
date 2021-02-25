# nonebot-plugin-styledstr

Nonebot 2 风格化字符串管理插件。

[![time tracker](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr.svg)](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr)
![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-styledstr)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonebot-plugin-styledstr)
[![CodeFactor](https://www.codefactor.io/repository/github/jks15satoshi/nonebot_plugin_styledstr/badge)](https://www.codefactor.io/repository/github/jks15satoshi/nonebot_plugin_styledstr)
[![codecov](https://codecov.io/gh/jks15satoshi/nonebot_plugin_styledstr/branch/main/graph/badge.svg?token=8M2AHA8J3M)](https://codecov.io/gh/jks15satoshi/nonebot_plugin_styledstr)
![GitHub](https://img.shields.io/github/license/jks15satoshi/nonebot_plugin_styledstr)

> 由于本人 Python 水平低下，因此源码可能会令人不适，烦请谅解。

## 介绍

风格化字符串管理，或称字符串资源管理，即通过字符串标签来标识和获取一个字符串内容。设计初衷是用于灵活控制机器人的输出内容。

### 字符串标签

字符串标签用以在风格预设文件中唯一标识一个字符串内容。字符串标签使用点记法表示层级结构。举个例子，如果一个字符串在预设文件中的层级结构是这样的：

````json
{
    "one": {
        "sample": {
            "structure": "something"
        }
    }
}
````

那么这个字符串 `something` 的标签即为 `one.sample.structure`。

### 风格预设

该插件可以通过不同的风格预设来切换相同字符串标签的内容，通过这种方式，你可以为你的 ~~GLADoS~~ 机器人加装各种“人格核心”，或者让它变成一个“语言通”（即国际化）。使用方法可以参考 [使用用例](docs/usage.md#用例为bot增添多种不同的语言风格)。

> 这也是为何我将这个插件命名为“风格化字符串管理”而非诸如“字符串资源管理”一类的名称（虽然这名称依旧很烂）。

## 安装

> 注意：Python 版本不应低于 3.9。

### 使用 `nb-cli` 安装

````shell
nb plugin install nonebot-plugin-styledstr
````

### 使用 Poetry 安装

````shell
poetry add nonebot-plugin-styledstr
````

### 使用 `pip` 安装

````shell
pip install nonebot-plugin-styledstr
````

## 使用准备

### 配置

> 注意：使用该插件前，请务必在项目中创建存放字符串资源的目录，并通过下面的配置项指定其为资源目录。关于如何设置插件配置项，参考 Nonebot 2 官方文档的 [基本配置](https://v2.nonebot.dev/guide/basic-configuration.html) 章节。

该插件可通过在配置文件中添加如下配置项对部分功能进行配置。

- **`STYLEDSTR_RESPATH`**：字符串资源目录，默认为当前工作目录（建议在 `bot.py` 文件中使用 `pathlib` 进行配置或使用绝对路径，若使用相对路径请确保工作目录为项目根目录。**建议手动配置。**）；
- **`STYLEDSTR_PRESET`**：风格预设，默认为 `default`。

### 为项目添加风格预设文件

在字符串资源目录下根据需要创建风格预设文件。风格预设文件以 YAML 或 JSON 文件存储，并需确保文件名与风格预设配置一致，文件名对大小写不敏感。例如若风格预设配置为 `default`，则需要保证字符串资源目录下存在文件名为 `default` 的 YAML 或 JSON 文件。

如果在资源目录下同时存在多个满足同一预设的文件（例如同时存在 `default.yaml` 与 `default.json`），则会按 `.json` > `.yaml` > `.yml` 的优先级读取文件。

### 加载插件并获取解析器对象

参考 Nonebot 2 官方文档的 [加载插件](https://v2.nonebot.dev/guide/loading-a-plugin.html) 章节，在项目中加载该插件。

该插件可以使用 `import` 或通过 `nonebot.plugin.require` 获取解析器。

使用 `import` 获取解析器需自行创建解析器对象：

````python
>>> from nonebot_plugin_styledstr import styledstr
# 使用 Nonebot 初始化时读取的配置
>>> parser = styledstr.Parser()
# 或使用自定义配置
>>> parser = styledstr.Parser(styledstr_preset='custom')
````

使用 `require` 方式获取解析器时，若无需自定义配置可直接获取解析器对象：

````python
>>> from nonebot import require
>>> parser = require('nonebot_plugin_styledstr').parser
````

若需要自定义配置也可通过以下方式创建解析器对象：

````python
>>> from nonebot import require
# 方式 1
>>> import nonebot
>>> config = nonebot.get_driver().config
>>> config.styledstr_preset = 'custom'
>>> parser = require('nonebot_plugin_styledstr').init(config)
# 方式 2
>>> from pathlib import Path
>>> config = {
...     'styledstr_respath': Path('path/to/respath'),
...     'styledstr_preset': 'custom'
... }
>>> parser = require('nonebot_plugin_styledstr').init(config)
````

## 使用

参见 [使用用例](docs/usage.md) 了解该插件的用法。

## 许可协议

该项目以 MIT 协议开放源代码，详阅 [LICENSE](LICENSE) 文件。
