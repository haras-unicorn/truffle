from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
  @abstractmethod
  def trace(self, msg: str, obj: Any | None = None) -> None:
    pass

  @abstractmethod
  def debug(self, msg: str, obj: Any | None = None) -> None:
    pass

  @abstractmethod
  def info(self, msg: str, obj: Any | None = None) -> None:
    pass

  @abstractmethod
  def warn(self, msg: str, obj: Any | None = None) -> None:
    pass

  @abstractmethod
  def err(self, msg: str, obj: Any | None = None) -> None:
    pass

  @abstractmethod
  def crit(self, msg: str, obj: Any | None = None) -> None:
    pass
