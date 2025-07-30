import json
from enum import Enum
from typing import Any, List

import tomlkit
import yaml


class Format(str, Enum):
  TOML = "toml"
  YAML = "yaml"
  JSON = "json"

  @property
  def type(self) -> str:
    return self.value

  @property
  def extension(self) -> str:
    return self.value

  @property
  def extensions(self) -> List[str]:
    if self is Format.TOML:
      return ["toml"]
    elif self is Format.YAML:
      return ["yaml", "yml"]
    elif self is Format.JSON:
      return ["json"]

    raise ValueError(f"Unsupported format: {self}")

  @classmethod
  def from_extension(cls, extension: str) -> "Format":
    if extension in Format.TOML.extensions:
      return Format.TOML
    elif extension in Format.YAML.extensions:
      return Format.YAML
    elif extension in Format.JSON.extensions:
      return Format.JSON

    raise ValueError(f"Unsupported format extension: {extension}")

  @classmethod
  def from_suffix(cls, suffix: str) -> "Format":
    return cls.from_extension(suffix.removeprefix("."))

  @classmethod
  def from_type(cls, type: str) -> "Format":
    if type == Format.TOML.type:
      return Format.TOML
    elif type == Format.YAML.type:
      return Format.YAML
    elif type == Format.JSON.type:
      return Format.JSON

    raise ValueError(f"Unsupported format type: {type}")

  def deserialize(self, serialized: str) -> Any:
    if self is Format.TOML:
      return tomlkit.loads(serialized)
    elif self is Format.YAML:
      return yaml.safe_load(serialized)
    elif self is Format.JSON:
      return json.loads(serialized)

    raise ValueError(f"Unsupported format: {self}")

  def serialize(self, deserialized: Any) -> str:
    if self is Format.TOML:
      return tomlkit.dumps(deserialized)
    elif self is Format.YAML:
      return yaml.safe_dump(deserialized)
    elif self is Format.JSON:
      return json.dumps(deserialized)

    raise ValueError(f"Unsupported format: {self}")
