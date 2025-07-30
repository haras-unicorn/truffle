from abc import ABC, abstractmethod
from typing import Any


class Writer(ABC):
  @abstractmethod
  def write_job(self, job: Any) -> None:
    pass

  @abstractmethod
  def write_metadata(self, metadata: Any) -> None:
    pass
