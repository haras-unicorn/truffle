from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from truffle_cli.environment import Environment, LogLevel
from truffle_cli.format import Format
from truffle_cli.logger.abstract import Logger


class System(ABC):
  @abstractmethod
  def get_env_var(self, key: str, default: str | None = None) -> Optional[str]:
    pass

  @abstractmethod
  def get_env_vars(self) -> Dict[str, str]:
    pass

  @abstractmethod
  def get_args(self) -> List[str]:
    pass

  @abstractmethod
  def needs_help(self) -> bool:
    pass

  @abstractmethod
  def needs_schema(self) -> bool:
    pass

  @abstractmethod
  def takes_stdin(self) -> Optional[Format]:
    pass

  @abstractmethod
  def read_stdin(self) -> str:
    pass

  @abstractmethod
  def path_exists(self, path: str) -> bool:
    pass

  @abstractmethod
  def path_suffix(self, path: str) -> str:
    pass

  @abstractmethod
  def path_join(self, lhs: str, rhs: str) -> str:
    pass

  @abstractmethod
  def read_file(self, path: str) -> str:
    pass

  @abstractmethod
  def append_file(self, path: str, content: str) -> None:
    pass

  @abstractmethod
  def clear_file(self, path: str) -> None:
    pass

  @abstractmethod
  def write_stdout(self, content: str) -> None:
    pass

  @abstractmethod
  def get_config_dir(self) -> str:
    pass

  @abstractmethod
  def setup_logging(
    self, log_level: LogLevel, environment: Environment
  ) -> None:
    pass

  @abstractmethod
  def get_logger(self, name: str) -> Logger:
    pass
