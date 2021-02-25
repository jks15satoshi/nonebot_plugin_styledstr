from nonebot.log import logger


class StyledstrError(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def log(self) -> None:
        logger.opt(colors=True).error(f'<R><b>{self.message}</b></R>')


class ResourcePathError(StyledstrError):
    def __init__(self) -> None:
        super().__init__('Resource path is not specified in the configuration '
                         'file.')


class PresetFileError(StyledstrError):
    def __init__(self, /, preset='', *, message='') -> None:
        super().__init__('Cannot find any valid preset file in the resource '
                         f'path with preset {preset}.'
                         if not message else message)


class TokenError(StyledstrError):
    def __init__(self, /, token='', *, message='') -> None:
        super().__init__(f'Token "{token}" is regarded as invalid or '
                         'nonexistent and skipped parsing.'
                         if not message else message)
