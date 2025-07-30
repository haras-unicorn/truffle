from logging import Logger as PyLogger

from truffle_cli.environment import Environment
from truffle_cli.logger.abstract import Logger
from truffle_cli.logger.console import ConsoleLogger


def create(py_logger: PyLogger, environment: Environment) -> Logger:
  return ConsoleLogger(py_logger, environment)
