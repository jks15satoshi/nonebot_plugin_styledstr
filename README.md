# nonebot-plugin-styledstr

Nonebot 2 风格化字符串管理插件。

[![time tracker](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr.svg)](https://wakatime.com/badge/github/jks15satoshi/nonebot_plugin_styledstr)

> 由于本人 Python 水平低下，因此源码可能会令人不适，烦请谅解。

## 介绍

风格化字符串管理，或称字符串资源管理，即通过字符串标签来标识和获取一个字符串内容。设计初衷是用于灵活控制机器人的输出内容。

### 字符串标签

字符串标签用以在风格预设文件中唯一标识一个字符串内容。字符串标签使用点记法表示层级结构。举个例子，如果一个字符串在预设文件中的层级结构是这样的：

````yaml
one:
    sample:
        structure: something
````

那么这个字符串 `something` 的标签即为 `one.sample.structure`。

### 占位符

如果字符串中的某些部分需要在运行时改变内容，那么可以在其中加入占位符，标记需要修改的部分。

占位符由两部分组成：用以标识占位符的占位符名称，以及包围占位符名称的指示符 `$`。占位符名称是由英文字母、数字与下划线组成的非空字符串，且首字符仅可为英文字母，长度不超过 24 个字符。例如 `$Placeholder_Here$`。

占位符名称对大小写不敏感，但在调用程序方法进行占位符替换时，占位符名称只能为小写字母（数字和下划线不受影响）。使用方法可以参考 [使用用例](#用例通过占位符替换文本内容)。

### 风格预设

该插件可以通过不同的风格预设来切换相同字符串标签的内容，通过这种方式，你可以为你的 ~~GLADoS~~ 机器人加装各种“人格核心”，或者让它变成一个“语言通”（即国际化）。使用方法可以参考 [使用用例](#用例通过风格预设切换不同风格的字符串内容)。

> 这也是为何我将这个插件命名为“风格化字符串管理”而非诸如“字符串资源管理”一类的名称（虽然这名称依旧很烂）。

## 安装

> 注意：Python 版本不应低于 3.8。

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

## 使用

### 配置

> 注意：使用该插件前，请务必在项目中创建存放字符串资源的目录，并通过下面的配置项指定其为资源目录。关于如何设置插件配置项，参考 Nonebot 2 官方文档的 [基本配置](https://v2.nonebot.dev/guide/basic-configuration.html) 章节。

该插件可通过在配置文件中添加如下配置项对部分功能进行配置。

- **`STYLEDSTR_RESPATH`**：字符串资源目录（**必填项**。建议在 `bot.py` 文件中使用 `pathlib` 进行配置或使用绝对路径，若使用相对路径请确保工作目录为项目根目录）；
- **`STYLEDSTR_PRESET`**：风格预设，默认为 `default`。

### 为项目添加风格预设文件

在上一节创建的字符串资源目录下根据需要创建风格预设文件。风格预设文件以 YAML 或 JSON 文件存储，并需确保文件名与风格预设配置一致，文件名对大小写不敏感。例如若风格预设配置为 `default`，则需要保证字符串资源目录下存在文件 `default.yaml` 或 `default.json`。

如果在资源目录下同时存在多个满足同一预设的文件（例如同时存在 `default.yaml` 与 `default.json`），则所读取的预设文件是不确定的，因此应避免出现此种情况。

### 加载插件并获取解析器对象

参考 Nonebot 2 官方文档的 [加载插件](https://v2.nonebot.dev/guide/loading-a-plugin.html) 章节，在项目中加载该插件。

使用前，请通过 `require` 获取 `parser` 解析器对象。

````python
>>> from nonebot import require
>>> parser = require('nonebot_plugin_styledstr').parser
# 调用 parse 方法解析字符串标签
>>> parser.parse('token.sample')
````

详细使用方法请见下面的 [使用用例](#使用用例) 部分。

## 使用用例

你可以通过以下用例来大致了解该插件的功能。

> 以下用例中出现的 Python 语句默认获取了该插件。

### 用例：通过风格预设切换不同风格的字符串内容

假设在你的项目目录下存在如下的风格预设文件：

````yaml
# default.yaml
help:
    prompt: 请输入你需要获取的帮助内容

# customer_service.yaml
help:
    prompt: 亲，请问您需要什么帮助？
````

则可以根据实际配置的风格预设，获取对应预设文件的字符串内容：

> 关于如何配置风格预设，请见 [配置](#配置) 一节。

````python
>>> parser.parse('help.prompt')
# STYLEDSTR_PRESET=DEFAULT
'请输入你需要获取的帮助内容'
# STYLEDSTR_PRESET=CUSTOMER_SERVICE
'亲，请问您需要什么帮助？'
````

或者强制以某个预设获取字符串内容：

````python
>>> parser.parse('help.prompt', preset='customer_service')
'亲，请问您需要什么帮助？'
````

类似地，也可以通过创建多语言预设实现国际化 (i18n) 功能。

### 用例：通过占位符替换文本内容

假设在你的项目目录下存在如下的风格预设文件：

````yaml
# default.yaml
demo:
    clock: 当前的时间为$TIME$。
````

则在该风格预设下，可以通过如下方式将占位符 `$TIME$` 替换为实际的时间：

````python
>>> from time import gmtime, strftime
>>> current_time = strftime(r'%Y年%m月%d日 %H:%M:%S', gmtime(1609459200))
>>> parser.parse('demo.clock', time=current_time)
'当前的时间为2021年1月1日 00:00:00。'
````

## 许可协议

该项目以 MIT 协议开放源代码，详阅 [LICENSE](LICENSE) 文件。
