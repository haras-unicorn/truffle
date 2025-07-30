import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, override

import tomlkit
import yaml

from truffle_cli.format import Format
from truffle_cli.system.abstract import System

from .abstract import Writer


@dataclass
class StdoutWriterConfig:
  format: Format


class StdoutWriter(Writer):
  _system: System
  _config: StdoutWriterConfig

  def __init__(self, system: System, config: StdoutWriterConfig):
    self._system = system
    self._config = config

  @override
  def write_job(self, job: Any) -> None:
    self._write(job)

  @override
  def write_metadata(self, metadata: Any) -> None:
    self._write(metadata)

  def _write(self, obj: Any) -> None:
    obj = asdict(obj) if is_dataclass(obj) else obj.__dict__  # type: ignore

    if self._config.format == Format.TOML:
      dump = tomlkit.dumps(obj)
      content = f"[[output]]\n{dump}\n"
      self._system.write_stdout(content)
    elif self._config.format == Format.YAML:
      dump = yaml.safe_dump(obj)
      content = f"{dump}\n---\n"
      self._system.write_stdout(content)
    elif self._config.format == Format.JSON:
      dump = json.dumps(obj)
      content = f"{dump}\n"
      self._system.write_stdout(content)
