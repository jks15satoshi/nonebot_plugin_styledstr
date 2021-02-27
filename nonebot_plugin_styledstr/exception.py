from nonebot.log import logger


class StyledstrError(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def log(self) -> None:
        logger.opt(colors=True).error(f'<R><b>{self.message}</b></R>')


class PresetFileError(StyledstrError):
    def __init__(self, /, preset=None, respath=None, *, message='') -> None:
        super().__init__(f'Cannot find any valid file of preset "{preset}" '
                         f'from the resource path {respath.absolute()}'
                         if not message else message)


class TokenError(StyledstrError):
    def __init__(self, /, token='', *, message='') -> None:
        super().__init__(f'Token "{token}" is regarded as invalid or '
                         'nonexistent and skipped parsing.'
                         if not message else message)
