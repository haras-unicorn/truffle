from dataclasses import dataclass
from typing import Dict, Final, Literal, Union

from truffle_cli.html_processor import HtmlProcessorConfig
from truffle_cli.llm_service import LlmServiceConfig
from truffle_cli.scraping_service import ScrapingServiceConfig

WorkerConfig = Union["SyncWorkerConfig"]


SYNC_WORKER_TYPE: Literal["sync"] = "sync"

SYNC_WORKER_SITE_MAX_PAGES: Final[int] = 50


@dataclass
class SyncWorkerConfig:
  sites: Dict[str, "SyncWorkerSiteConfig"]
  type: Literal["sync"] = SYNC_WORKER_TYPE


@dataclass
class SyncWorkerSiteConfig:
  base_url: str
  pagination: "PaginationSyncWorkerSiteConfig"
  scraping_service: ScrapingServiceConfig
  html_processor: HtmlProcessorConfig
  llm_service: LlmServiceConfig


@dataclass
class PaginationSyncWorkerSiteConfig:
  template: str
  start: int
  stop: int
  step: int
