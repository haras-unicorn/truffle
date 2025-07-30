import logging
from logging import Logger as PyLogger
from typing import Any, override

from truffle_cli.environment import Environment

from .abstract import Logger


class ConsoleLogger(Logger):
  TRACE_LEVEL = 5
  logging.addLevelName(TRACE_LEVEL, "trace")

  _logger: PyLogger
  _environment: Environment

  def __init__(self, logger: PyLogger, environment: Environment):
    self._logger = logger
    self._environment = environment

  @override
  def trace(self, msg: str, obj: Any | None = None) -> None:
    self._logger.log(ConsoleLogger.TRACE_LEVEL, msg, extra=obj)

  @override
  def debug(self, msg: str, obj: Any | None = None) -> None:
    self._logger.log(logging.DEBUG, msg, extra=obj)

  @override
  def info(self, msg: str, obj: Any | None = None) -> None:
    self._logger.log(logging.INFO, msg, extra=obj)

  @override
  def warn(self, msg: str, obj: Any | None = None) -> None:
    self._logger.log(logging.WARNING, msg, extra=obj)

  @override
  def err(self, msg: str, obj: Any | None = None) -> None:
    self._logger.log(
      logging.ERROR,
      msg,
      stack_info=self._environment == Environment.DEVELOPMENT,
      extra=obj,
    )

  @override
  def crit(self, msg: str, obj: Any | None = None) -> None:
    self._logger.log(
      logging.CRITICAL,
      msg,
      stack_info=self._environment == Environment.DEVELOPMENT,
      extra=obj,
    )
