from truffle_cli.http_client.abstract import HttpClient
from truffle_cli.system.abstract import System

from .abstract import ScrapingService
from .input import ZYTE_SCRAPING_SERVICE_TYPE, ScrapingServiceConfig
from .zyte import ZyteScrapingService


def create(
  system: System, config: ScrapingServiceConfig, client: HttpClient
) -> ScrapingService:
  if config.type == ZYTE_SCRAPING_SERVICE_TYPE:
    return ZyteScrapingService(system, config, client)
