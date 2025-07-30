from dataclasses import dataclass
from typing import Optional

from truffle_cli.format import Format
from truffle_cli.system.abstract import System

from .abstract import Writer
from .file import FileWriter, FileWriterConfig
from .stdout import StdoutWriter, StdoutWriterConfig


@dataclass
class WriterConfig:
  path: Optional[str]
  format: Format


def create(system: System, config: WriterConfig) -> Writer:
  if config.path is not None:
    path = config.path

    suffix = system.path_suffix(path).removeprefix(".")
    if suffix in Format.TOML.extensions:
      format = Format.TOML
    elif suffix in Format.YAML.extensions:
      format = Format.YAML
    elif suffix in Format.JSON.extensions:
      format = Format.JSON
    else:
      format = config.format

    return FileWriter(system, FileWriterConfig(config.path, format))
  else:
    return StdoutWriter(system, StdoutWriterConfig(config.format))
