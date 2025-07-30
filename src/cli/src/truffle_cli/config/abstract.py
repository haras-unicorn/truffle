from abc import ABC, abstractmethod
from typing import Optional

from truffle_cli.worker import WorkerConfig
from truffle_cli.writer import WriterConfig

from .input import Config


class Loader(ABC):
  @abstractmethod
  def help(self) -> str:
    pass

  @abstractmethod
  def schema(self) -> str:
    pass

  @abstractmethod
  def load(self) -> Optional[Config]:
    pass

  @abstractmethod
  def for_worker(self, config: Config) -> WorkerConfig:
    pass

  @abstractmethod
  def for_writer(self, config: Config) -> WriterConfig:
    pass
