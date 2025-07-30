import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, override

import platformdirs

from truffle_cli.environment import Environment, LogLevel
from truffle_cli.format import Format
from truffle_cli.logger.abstract import Logger
from truffle_cli.logger.console import ConsoleLogger

from .abstract import System


class PlatformSystem(System):
  _environment: Environment = Environment.PRODUCTION

  @override
  def get_env_var(self, key: str, default: str | None = None) -> Optional[str]:
    return os.getenv(key, default)

  @override
  def get_env_vars(self) -> Dict[str, str]:
    return {item[0]: item[1] for item in os.environ.items()}

  @override
  def get_args(self) -> List[str]:
    return sys.argv[1:]

  @override
  def needs_help(self) -> bool:
    return "--help" in sys.argv[1:] or "-h" in sys.argv[1:]

  @override
  def needs_schema(self) -> bool:
    return "--schema" in sys.argv[1:]

  @override
  def takes_stdin(self) -> Optional[Format]:
    args = self.get_args()
    try:
      index = args.index("--stdin")
    except ValueError:
      return None

    return Format.from_type(args[index + 1])

  @override
  def read_stdin(self) -> str:
    return sys.stdin.read()

  @override
  def path_exists(self, path: str) -> bool:
    return Path(path).exists()

  @override
  def path_suffix(self, path: str) -> str:
    return Path(path).suffix

  @override
  def path_join(self, lhs: str, rhs: str) -> str:
    return str(Path(lhs) / rhs)

  @override
  def read_file(self, path: str) -> str:
    with open(path, "r") as file:
      return file.read()

  @override
  def append_file(self, path: str, content: str) -> None:
    with open(path, "a") as file:
      file.write(content)

  @override
  def clear_file(self, path: str) -> None:
    platform_path = Path(path)
    if platform_path.exists():
      with open(path, "w") as file:
        file.write("")
    else:
      platform_path.touch()

  @override
  def write_stdout(self, content: str) -> None:
    print(content)

  @override
  def get_config_dir(self) -> str:
    return platformdirs.user_config_dir()

  @override
  def setup_logging(
    self, log_level: LogLevel, environment: Environment
  ) -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
      root_logger.removeHandler(handler)

    self._environment = environment

    if log_level == LogLevel.TRACE:
      level = ConsoleLogger.TRACE_LEVEL
    else:
      level = getattr(logging, log_level.value.upper())

    logging.basicConfig(
      level=level,
      # spell-checker: disable-next-line
      format="[%(asctime)s.%(msecs)03d][%(name)s][%(levelname)s] %(message)s",
      datefmt="%Y-%m-%dT%H:%M:%S",
      handlers=[logging.StreamHandler(sys.stderr)],
    )

  @override
  def get_logger(self, name: str) -> Logger:
    return ConsoleLogger(logging.getLogger(name), self._environment)
