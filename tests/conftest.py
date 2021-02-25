import logging
import os
import sys
from pathlib import Path
from typing import Any, Generator

import nonebot
import pytest
from _pytest.logging import caplog as _caplog
from loguru import logger
from nonebot import require


sys.path.insert(0, os.path.abspath('../nonebot_plugin_styledstr'))


@pytest.fixture(scope='class')
def setup() -> None:
    config = {
        'styledstr_respath': Path(__file__).parent / 'assets',
        'styledstr_preset': 'test'
    }
    nonebot.init(**config)

    nonebot.load_plugin('nonebot_plugin_styledstr')


@pytest.fixture(scope='class')
def get_parser(request, setup) -> Generator[Any, None, None]:
    parser = require('nonebot_plugin_styledstr').parser

    if request.cls:
        request.cls.parser = parser
    yield parser


@pytest.fixture()
def caplog(_caplog, request) -> Generator[Any, None, None]:
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format='{message} {extra}')

    if request.cls:
        request.cls.caplog = _caplog

    yield _caplog
    logger.remove(handler_id)
