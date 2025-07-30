from abc import ABC, abstractmethod
from typing import Generator

from .output import OutputJob, OutputMetadata


class Worker(ABC):
  @abstractmethod
  def run(self) -> Generator[OutputJob, None, OutputMetadata]:
    pass
