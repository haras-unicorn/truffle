from dataclasses import dataclass
from typing import Literal, Union

ScrapingServiceConfig = Union["ZyteScrapingServiceConfig"]


ZYTE_SCRAPING_SERVICE_TYPE: Literal["zyte"] = "zyte"


@dataclass
class ZyteScrapingServiceConfig:
  base_url: str
  api_key: str
  requires_browser: bool
  list_payload: dict
  details_payload: dict
  type: Literal["zyte"] = ZYTE_SCRAPING_SERVICE_TYPE
