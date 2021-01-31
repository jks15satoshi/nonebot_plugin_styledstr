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
    def __init__(self, preset: str) -> None:
        super().__init__(f'Preset file {preset}.yaml is not found in the '
                         'resource path.')


class TokenError(StyledstrError):
    def __init__(self, token: str) -> None:
        super().__init__(f'Token "{token}" is not found so cannot be parsed.')
