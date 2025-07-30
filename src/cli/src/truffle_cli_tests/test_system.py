import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Literal, Optional, override

import tomlkit
import yaml
from truffle_cli.config.system import CONFIG_FILE_NAME, ENV_PREFIX
from truffle_cli.environment import Environment, LogLevel
from truffle_cli.format import Format
from truffle_cli.logger.abstract import Logger
from truffle_cli.system.abstract import System

from .test_logger import TestLog, TestLogger


class TestSystem(System):
  __test__ = False

  CURRENT_DIR: Literal["/"] = "/"
  CONFIG_DIR: Literal["/config"] = "/config"

  args: List[str]
  env: Dict[str, str]
  files: Dict[str, str]
  logs: List[TestLog]
  stdin: str
  stdout: str
  log_level: LogLevel
  environment: Environment

  def __init__(
    self, args: List[str], env: Dict[str, str], files: Dict[str, str]
  ):
    self.args = args
    self.env = env
    self.files = files
    self.logs = []
    self.stdout = ""
    self.log_level = LogLevel.INFO

  def __repr__(self) -> str:
    result = ""
    result += "Args:"
    for arg in self.args:
      result += f"\n{arg}"

    result += "\n\n\nEnv:"
    for key, value in self.env.items():
      result += f"\n{key} = {value}"

    result += "\n\n\nFiles:"
    for path, content in self.files.items():
      result += f"\n\n{path}:\n{content}EOF"

    result += "\n\n\nLogs:"
    for log in self.logs:
      if log.trace is not None:
        if log.obj is not None:
          obj = log.obj
          if hasattr(log.obj, "__dict__"):
            obj = log.obj.__dict__
          result += f"\n\n[{log.time}][{log.name}][{log.level}]: {log.msg}\n\n{json.dumps(obj, indent=True)}\n\n{log.trace}"
        else:
          result += (
            f"\n\n[{log.time}][{log.name}][{log.level}]: {log.msg}\n{log.trace}"
          )
      else:
        if log.obj is not None:
          obj = log.obj
          if hasattr(log.obj, "__dict__"):
            obj = log.obj.__dict__
          result += f"\n\n[{log.time}][{log.name}][{log.level}]: {log.msg}\n{json.dumps(obj, indent=True)}"
        else:
          result += f"\n\n[{log.time}][{log.name}][{log.level}]: {log.msg}"

    result += "\n"
    return result

  def __str__(self) -> str:
    return self.__repr__()

  def set_env(self, name: str, value: str) -> None:
    self.env[f"{ENV_PREFIX}_{name.upper()}"] = value

  def set_arg(self, name: str, value: str | None = None) -> None:
    self.args.append(name)
    if value is not None:
      self.args.append(value)

  def set_file(
    self, value: dict, path: str, type: Format = Format.TOML
  ) -> None:
    self._set_file(value, type, path)

  def set_config_file(self, value: dict, type: Format = Format.TOML) -> None:
    path = f"{CONFIG_FILE_NAME}.{type.extension}"
    self._set_file(value, type, path)

  def _set_file(self, value: dict, type: Format, path: str | None) -> None:
    if path is None:
      path = f"{CONFIG_FILE_NAME}.{type.extension}"

    if type == Format.TOML:
      str_value = tomlkit.dumps(value)
    elif type == Format.YAML:
      str_value = yaml.safe_dump(value)
    elif type == Format.JSON:
      str_value = json.dumps(value)

    self.files[path] = str_value

  def set_stdin(
    self,
    value: dict,
    type: Format = Format.TOML,
  ) -> None:
    if type == Format.TOML:
      str_value = tomlkit.dumps(value)
    elif type == Format.YAML:
      str_value = yaml.safe_dump(value)
    elif type == Format.JSON:
      str_value = json.dumps(value)

    self.stdin = str_value

  @override
  def get_env_var(self, key: str, default: str | None = None) -> Optional[str]:
    return self.env.get(key, default)

  @override
  def get_env_vars(self) -> Dict[str, str]:
    return self.env

  @override
  def get_args(self) -> List[str]:
    return self.args

  @override
  def needs_help(self) -> bool:
    return "--help" in self.args or "-h" in self.args or len(self.args) == 0

  @override
  def needs_schema(self) -> bool:
    return "--schema" in self.args

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
    return self.stdin

  @override
  def path_exists(self, path: str) -> bool:
    return path in self.files

  @override
  def path_suffix(self, path: str) -> str:
    return Path(path).suffix

  @override
  def path_join(self, lhs: str, rhs: str) -> str:
    return str(Path(lhs) / rhs)

  @override
  def read_file(self, path: str) -> str:
    text = self.files.get(path)
    if text is None:
      raise FileNotFoundError(f"File {path} not found")
    return text

  @override
  def append_file(self, path: str, content: str) -> None:
    text = self.files.get(path)
    if text is None:
      raise FileNotFoundError(f"File {path} not found")
    text += content

  @override
  def clear_file(self, path: str) -> None:
    self.files[path] = ""

  @override
  def write_stdout(self, content: str) -> None:
    self.stdout += content

  @override
  def get_config_dir(self) -> str:
    return TestSystem.CONFIG_DIR

  @override
  def setup_logging(
    self, log_level: LogLevel, environment: Environment
  ) -> None:
    self.log_level = log_level
    self.environment = environment
    self.logs.append(
      TestLog(
        datetime.now(timezone.utc),
        __name__,
        LogLevel.DEBUG,
        f'Log level set to: "{log_level.value}"',
        None,
        None,
      )
    )

  @override
  def get_logger(self, name: str) -> Logger:
    return TestLogger(lambda log: self.logs.append(log), name)
