# 使用用例

本文档将列举出几个使用用例，以便理解该插件的使用方法。

> 以下用例中出现的 Python 语句默认获取了该插件。

## 用例：为 bot 增添多种不同的风格

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

> 关于如何配置风格预设，请见 [配置](../README.md#配置) 一节。

````python
>>> parser.parse('help.prompt')
# STYLEDSTR_PRESET=DEFAULT
'请输入你需要获取的帮助内容'
# STYLEDSTR_PRESET=CUSTOMER_SERVICE
'亲，请问您需要什么帮助？'
````

> **注意：** 解析时请确保字符串标签所对应的值类型为字符串。

获取字符串内容时也可以特别指定读取的风格预设，而无需被限制在初始化时的配置：

````python
# STYLEDSTR_PRESET=DEFAULT
>>> parser.parse('help.prompt', preset='custom_service')
'亲，请问您需要什么帮助？'
````

> **注意：**
>
> 你可以使用预设名称（如上例）或者风格预设文件路径指定解析时读取的风格预设：
>
> - 指定为预设名称时，将会在资源目录下查找符合指定预设名称的文件读取；
> - 以预设文件的后缀名结尾的字符串将首先视为文件的绝对路径尝试读取；如判断该文件不存在时则视为文件的相对路径，此时将会在资源目录下查找该文件进行读取；
> - 以 `pathlib.Path` 对象指定将视为文件的绝对路径，此时将尝试直接读取所指定的文件。

## 用例：使用占位符动态变更文本内容

如果你的预设文本中有部分内容需要动态更改，你可以使用占位符将需要变更的地方标记出来。

占位符由占位符名称与包围占位符名称的分界符 `$` 组成，其中占位符名称用以唯一标识一个占位符，可使用包括英文字母、数字以及下划线组成的、长度不大于 24 个字符且首字符仅可为英文字母的非空字符串命名，例如 `$Placeholder_here$`。

占位符名称对大小写不敏感，但在执行替换时，只能使用小写的占位符名称作为参数（数字和下划线不受影响）。

> **注意：**
>
> - 无效的占位符将被视为常规的文本信息；
> - 由于方法实现原因，`contents`、`preset` 和 `token` 也将被视为无效的占位符名称。

假设你需要将当前时间包装为预设文件中规定的格式，那么就可以在文本中加入占位符：

````yaml
# default.yaml
time:
    report: 当前时间为$TIME$。
````

然后在获取时将占位符 `$TIME$` 替换为当前时间：

````python
>>> from datetime import datetime
>>> time = datetime.utcfromtimestamp(1609459200)
>>> parser.parse('time.report', time=time.strftime(r'%Y年%m月%d日 %H:%M:%S'))
'当前时间为2021年1月1日 00:00:00。'
````
