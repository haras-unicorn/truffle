from dataclasses import dataclass
from typing import Dict, Literal, Optional, Union

from truffle_cli.environment import Environment, LogLevel
from truffle_cli.format import Format


@dataclass
class Config:
  args: "ArgsConfig"
  env: "EnvConfig"
  file: "FileConfig"


@dataclass
class ArgsConfig:
  """
  Truffle CLI

  A job hunting tool that forages through job boards, using AI to uncover and
  score the most valuable opportunities hidden beneath the surface.
  """

  # Print help
  help: bool = False
  # Print file config json schema
  schema: bool = False
  # Print version
  version: bool = False
  # Set log level (trace, debug, info, warning, error, critical)
  log_level: LogLevel = LogLevel.INFO
  # Read file config from stdin
  stdin: bool = False
  # Read file config from given path
  config_path: Optional[str] = None
  # Write output to given path
  output_path: Optional[str] = None
  # Write output in given format
  output_format: Optional[Format] = None


@dataclass
class EnvConfig:
  config_log_level: LogLevel = LogLevel.ERROR
  environment: Environment = Environment.PRODUCTION
  zyte_api_key: Optional[str] = None
  openai_api_key: Optional[str] = None
  cv: Optional[str] = None


@dataclass
class FileConfig:
  scraping_service: "ScrapingServiceFileConfig"
  llm_service: "LlmServiceFileConfig"
  worker: "WorkerFileConfig"
  sites: Dict[str, "SiteFileConfig"]
  max_pages: int = 50


@dataclass
class SiteFileConfig:
  base_url: str
  pagination: "PaginationSiteFileConfig"
  scraping_service: Optional["ScrapingServiceFileConfig"]
  html_processor: "HtmlProcessorFileConfig"
  llm_service: Optional["LlmServiceFileConfig"]


@dataclass
class PaginationSiteFileConfig:
  template: str
  start: int = 0
  stop: int = 50
  step: int = 1


WorkerFileConfig = Union["SyncWorkerFileConfig"]


SYNC_WORKER_CONFIG_FILE_TYPE: Literal["sync"] = "sync"


@dataclass
class SyncWorkerFileConfig:
  type: Literal["sync"] = SYNC_WORKER_CONFIG_FILE_TYPE


ScrapingServiceFileConfig = Union["ZyteScrapingServiceFileConfig"]


ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE: Literal["zyte"] = "zyte"


@dataclass
class ZyteScrapingServiceFileConfig:
  base_url: str
  api_key: Optional[str] = None
  requires_browser: bool = False
  list_payload: Optional[dict] = None
  details_payload: Optional[dict] = None
  type: Literal["zyte"] = ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE


HtmlProcessorFileConfig = Union["BeautifulSoupHtmlProcessorFileConfig"]


BEAUTIFUL_SOUP_HTML_PROCESSOR_FILE_CONFIG_TYPE: Literal["beautiful-soup"] = (
  "beautiful-soup"
)


@dataclass
class BeautifulSoupHtmlProcessorFileConfig:
  link_selector: str
  title_selector: str
  details_selector: str
  type: Literal["beautiful-soup"] = (
    BEAUTIFUL_SOUP_HTML_PROCESSOR_FILE_CONFIG_TYPE
  )


LlmServiceFileConfig = Union["OpenaiLlmServiceFileConfig"]


OPENAI_LLM_SERVICE_FILE_CONFIG_TYPE: Literal["openai"] = "openai"


@dataclass
class OpenaiLlmServiceFileConfig:
  base_url: str
  model: str
  extraction_prompt: str
  summary_prompt: str
  scoring_prompt: str
  cv: Optional[str] = None
  api_key: Optional[str] = None
  thinking_regex: Optional[str] = None
  type: Literal["openai"] = OPENAI_LLM_SERVICE_FILE_CONFIG_TYPE
