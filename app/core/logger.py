from __future__ import annotations

import sys
from typing import TextIO

from loguru import logger

from app.core.config import settings


def _log_format(record: dict) -> str:
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>\n"
    )


def setup_logger(sink: TextIO | str = sys.stderr) -> None:
    logger.remove()
    logger.add(
        sink,
        format=_log_format,
        level=settings.LOG_LEVEL.upper(),
        colorize=True,
        backtrace=True,
        diagnose=settings.DEBUG,
        enqueue=True,
    )
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        format=_log_format,
        level=settings.LOG_LEVEL.upper(),
        rotation="00:00",
        retention="30 days",
        compression="gz",
        enqueue=True,
    )


setup_logger()
