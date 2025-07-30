from typing import Any, Dict, override

import requests

from truffle_cli.logger.abstract import Logger
from truffle_cli.system.abstract import System

from .abstract import HttpClient


class RequestsHttpClient(HttpClient):
  _system: System
  _logger: Logger

  def __init__(self, system: System):
    self._system = system

    self._logger = self._system.get_logger(__name__)

  @override
  def post(self, url: str, headers: Dict[str, str], payload: Any) -> Any:
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
      raise Exception(
        f"{url} responded with {response.status_code} - {response.text}"
      )

    self._logger.trace(f"Posted: '{url}'")

    return response.json()
