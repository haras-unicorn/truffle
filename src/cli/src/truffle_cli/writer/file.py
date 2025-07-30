import json
import textwrap
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, override

import tomlkit
import yaml

from truffle_cli.format import Format
from truffle_cli.system.abstract import System

from .abstract import Writer


@dataclass
class FileWriterConfig:
  path: str
  format: Format


class FileWriter(Writer):
  _system: System
  _config: FileWriterConfig

  def __init__(self, system: System, config: FileWriterConfig):
    self._system = system
    self._config = config

    self._system.clear_file(self._config.path)
    if self._config.format == Format.YAML:
      self._system.append_file(self._config.path, "output:\n")
    elif self._config.format == Format.JSON:
      self._system.append_file(self._config.path, '{"output":[')

  @override
  def write_job(self, job: Any) -> None:
    self._write(job)

  @override
  def write_metadata(self, metadata: Any) -> None:
    self._write_last(metadata)

  def _write(self, obj: Any) -> None:
    obj = asdict(obj) if is_dataclass(obj) else obj.__dict__  # type: ignore

    if self._config.format == Format.TOML:
      dump = tomlkit.dumps(obj)
      content = f"[[output]]\n{dump}\n"
      self._system.append_file(self._config.path, content)
    elif self._config.format == Format.YAML:
      dump = yaml.safe_dump(obj)
      content = textwrap.indent(dump, "    ")
      content = f"  - {content[4:]}\n"
      self._system.append_file(self._config.path, content)
    elif self._config.format == Format.JSON:
      dump = json.dumps(obj)
      content = f"{dump},"
      self._system.append_file(self._config.path, content)

  def _write_last(self, obj: Any) -> None:
    obj = asdict(obj) if is_dataclass(obj) else obj.__dict__  # type: ignore

    if self._config.format == Format.TOML:
      dump = tomlkit.dumps(obj)
      content = f"[[output]]\n{dump}"
      self._system.append_file(self._config.path, content)
    elif self._config.format == Format.YAML:
      dump = yaml.safe_dump(obj)
      content = textwrap.indent(dump, "    ")
      content = f"  - {content[4:]}"
      self._system.append_file(self._config.path, content)
    elif self._config.format == Format.JSON:
      dump = json.dumps(obj)
      content = f"{dump}]}}"
      self._system.append_file(self._config.path, content)
