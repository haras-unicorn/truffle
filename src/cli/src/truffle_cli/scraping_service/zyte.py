from base64 import b64decode, b64encode
from typing import override

from truffle_cli.http_client import HttpClient
from truffle_cli.logger.abstract import Logger
from truffle_cli.system.abstract import System

from .abstract import ScrapingService
from .input import ZyteScrapingServiceConfig


class ZyteScrapingService(ScrapingService):
  _config: ZyteScrapingServiceConfig
  _client: HttpClient
  _system: System
  _logger: Logger

  def __init__(
    self, system: System, config: ZyteScrapingServiceConfig, client: HttpClient
  ):
    self._config = config
    self._client = client
    self._system = system

    self._logger = self._system.get_logger(__name__)

  @override
  def list(self, url: str) -> str:
    return self._call(url, self._config.list_payload)

  @override
  def details(self, url: str) -> str:
    return self._call(url, self._config.details_payload)

  def _call(self, url: str, additional_payload: dict) -> str:
    auth = b64encode(f"{self._config.api_key}:".encode()).decode()

    headers = {
      "Authorization": f"Basic {auth}",
      "Content-Type": "application/json",
    }

    payload = {
      "url": url,
      "httpResponseBody": not self._config.requires_browser,
      "browserHtml": self._config.requires_browser,
      **additional_payload,
    }

    response = self._client.post(str(self._config.base_url), headers, payload)

    if self._config.requires_browser:
      body = response["browserHtml"]
    else:
      body = b64decode(response["httpResponseBody"]).decode()

    self._logger.debug(f"Scraped: '{url}'")

    return body
