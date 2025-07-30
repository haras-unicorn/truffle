import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Optional, override

from truffle_cli.environment import LogLevel
from truffle_cli.logger.abstract import Logger


@dataclass
class TestLog:
  __test__ = False

  time: datetime
  name: str
  level: LogLevel
  msg: str
  trace: Optional[str]
  obj: Optional[Any]


class TestLogger(Logger):
  __test__ = False

  log: Callable[[TestLog], None]
  name: str

  def __init__(self, log: Callable[[TestLog], None], name: str):
    self.log = log
    self.name = name

  @override
  def trace(self, msg: str, obj: Any | None = None) -> None:
    self.log(
      TestLog(
        datetime.now(timezone.utc), self.name, LogLevel.TRACE, msg, None, obj
      )
    )

  @override
  def debug(self, msg: str, obj: Any | None = None) -> None:
    self.log(
      TestLog(
        datetime.now(timezone.utc), self.name, LogLevel.DEBUG, msg, None, obj
      )
    )

  @override
  def info(self, msg: str, obj: Any | None = None) -> None:
    self.log(
      TestLog(
        datetime.now(timezone.utc), self.name, LogLevel.INFO, msg, None, obj
      )
    )

  @override
  def warn(self, msg: str, obj: Any | None = None) -> None:
    self.log(
      TestLog(
        datetime.now(timezone.utc), self.name, LogLevel.WARNING, msg, None, obj
      )
    )

  @override
  def err(self, msg: str, obj: Any | None = None) -> None:
    self.log(
      TestLog(
        datetime.now(timezone.utc),
        self.name,
        LogLevel.ERROR,
        msg,
        traceback.format_exc(),
        obj,
      )
    )

  @override
  def crit(self, msg: str, obj: Any | None = None) -> None:
    self.log(
      TestLog(
        datetime.now(timezone.utc),
        self.name,
        LogLevel.CRITICAL,
        msg,
        traceback.format_exc(),
        obj,
      )
    )
