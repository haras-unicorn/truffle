import io
import json
from typing import Any, Final, List, Optional, override

import apischema
import dacite
import simple_parsing
from omegaconf import OmegaConf
from omegaconf import ValidationError as OmegaconfValidationError

from truffle_cli.environment import Environment, LogLevel
from truffle_cli.format import Format
from truffle_cli.html_processor.input import (
  BEAUTIFUL_SOUP_HTML_PROCESSOR_TYPE,
  BeautifulSoupHtmlProcessorConfig,
)
from truffle_cli.llm_service.input import (
  OPENAI_LLM_SERVICE_TYPE,
  OpenaiLlmServiceConfig,
)
from truffle_cli.logger.abstract import Logger
from truffle_cli.scraping_service.input import (
  ZYTE_SCRAPING_SERVICE_TYPE,
  ZyteScrapingServiceConfig,
)
from truffle_cli.system.abstract import System
from truffle_cli.worker.input import (
  SYNC_WORKER_TYPE,
  PaginationSyncWorkerSiteConfig,
  SyncWorkerConfig,
  SyncWorkerSiteConfig,
  WorkerConfig,
)
from truffle_cli.writer import WriterConfig

from .abstract import Loader
from .input import (
  BEAUTIFUL_SOUP_HTML_PROCESSOR_FILE_CONFIG_TYPE,
  OPENAI_LLM_SERVICE_FILE_CONFIG_TYPE,
  ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE,
  ArgsConfig,
  Config,
  EnvConfig,
  FileConfig,
)
from .static import STATIC_CONFIG

ENV_PREFIX = "TRUFFLE_CLI"
CONFIG_FILE_NAME: Final[str] = "truffle-cli"
CONFIG_FILE_EXTENSIONS: Final[List[str]] = []
for format in Format:
  for extension in format.extensions:
    CONFIG_FILE_EXTENSIONS.append(extension)


class SystemLoader(Loader):
  _system: System
  _logger: Logger

  def __init__(self, system: System):
    self._system = system
    self._logger = system.get_logger(__name__)

  @override
  def load(self) -> Optional[Config]:
    config_log_level = self._system.get_env_var(
      f"{ENV_PREFIX}_CONFIG_LOG_LEVEL"
    )
    if config_log_level is not None:
      self._system.setup_logging(
        LogLevel(config_log_level), Environment.DEVELOPMENT
      )
    else:
      self._system.setup_logging(LogLevel.ERROR, Environment.PRODUCTION)

    try:
      config = self._load()
    except OmegaconfValidationError as error:
      self._logger.err(f"Failed merging config - {error}")
      return None
    except Exception as error:
      self._logger.err(f"Failed loading config - {error}")
      return None

    if config.args.log_level is None:
      if config.args.environment is Environment.DEVELOPMENT:
        self._system.setup_logging(LogLevel.DEBUG, config.env.environment)
      else:
        self._system.setup_logging(LogLevel.INFO, config.env.environment)
    else:
      self._system.setup_logging(config.args.log_level, config.env.environment)

    return config

  def _load(self) -> Config:
    args = self._system.get_args()
    parser = simple_parsing.ArgumentParser(add_help=False)
    parser.add_arguments(dataclass=ArgsConfig, dest="config")
    args_config = parser.parse_args(args).config

    env_config = EnvConfig()
    env_config.zyte_api_key = self._system.get_env_var(
      f"{ENV_PREFIX}_ZYTE_API_KEY"
    )
    env_config.openai_api_key = self._system.get_env_var(
      f"{ENV_PREFIX}_OPENAI_API_KEY"
    )
    environment = self._system.get_env_var(f"{ENV_PREFIX}_ENVIRONMENT")
    if environment is not None:
      env_config.environment = Environment(environment)
    config_log_level = self._system.get_env_var(
      f"{ENV_PREFIX}_CONFIG_LOG_LEVEL"
    )
    if config_log_level is not None:
      env_config.config_log_level = LogLevel(config_log_level)
    env_config.cv = self._system.get_env_var(f"{ENV_PREFIX}_CV")

    dynamic_config_path = self._find_dynamic_config(args_config.config_path)
    if dynamic_config_path:
      self._logger.debug(f"Reading config from {dynamic_config_path}")
    dynamic_config = (
      self._load_file_config(dynamic_config_path) if dynamic_config_path else {}
    )
    merger = OmegaConf.create({})
    merger = OmegaConf.merge(merger, STATIC_CONFIG)
    merger = OmegaConf.merge(merger, dynamic_config)
    final_config = self._check_and_convert_to_dict(
      OmegaConf.to_container(merger)
    )
    file_config = dacite.from_dict(data_class=FileConfig, data=final_config)

    return Config(args_config, env_config, file_config)

  @override
  def help(self) -> str:
    parser = simple_parsing.ArgumentParser(add_help=False)
    parser.add_arguments(dataclass=ArgsConfig, dest="config")
    buffer = io.StringIO()
    parser.print_help(file=buffer)
    buffer.seek(0)
    help = buffer.read()
    return help

  @override
  def schema(self) -> str:
    schema = apischema.json_schema.deserialization_schema(FileConfig)
    return json.dumps(schema, indent=True)

  @override
  def for_worker(self, config: Config) -> WorkerConfig:
    if config.file.worker.type == "sync":
      site_configs = {}
      for site_name, site_file_config in config.file.sites.items():
        if site_file_config.scraping_service is None:
          file_scraping_service = config.file.scraping_service
        else:
          file_scraping_service = site_file_config.scraping_service

        if file_scraping_service.type == ZYTE_SCRAPING_SERVICE_FILE_CONFIG_TYPE:
          api_key = config.env.zyte_api_key or file_scraping_service.api_key
          if api_key is None:
            raise ValueError("API key not set for Zyte scraping service")
          scraping_service = ZyteScrapingServiceConfig(
            base_url=file_scraping_service.base_url,
            api_key=api_key,
            requires_browser=file_scraping_service.requires_browser,
            list_payload=file_scraping_service.list_payload or {},
            details_payload=file_scraping_service.details_payload or {},
            type=ZYTE_SCRAPING_SERVICE_TYPE,
          )
        else:
          raise ValueError(
            f"Unknown scraping service {file_scraping_service.type}"
          )

        if (
          site_file_config.html_processor.type
          == BEAUTIFUL_SOUP_HTML_PROCESSOR_FILE_CONFIG_TYPE
        ):
          html_processor = BeautifulSoupHtmlProcessorConfig(
            link_selector=site_file_config.html_processor.link_selector,
            title_selector=site_file_config.html_processor.title_selector,
            details_selector=site_file_config.html_processor.details_selector,
            type=BEAUTIFUL_SOUP_HTML_PROCESSOR_TYPE,
          )
        else:
          raise ValueError(
            f"Unknown html processor {site_file_config.html_processor.type}"
          )

        if site_file_config.llm_service is None:
          file_llm_service = config.file.llm_service
        else:
          file_llm_service = site_file_config.llm_service

        if file_llm_service.type == OPENAI_LLM_SERVICE_FILE_CONFIG_TYPE:
          api_key = config.env.openai_api_key or file_llm_service.api_key
          if api_key is None:
            raise ValueError("API key not set for OpenAI API service")
          cv = config.env.cv or file_llm_service.cv
          if cv is None:
            raise ValueError("CV not set")
          llm_service = OpenaiLlmServiceConfig(
            base_url=file_llm_service.base_url,
            api_key=api_key,
            model=file_llm_service.model,
            cv=self._read_if_path(cv),
            extraction_prompt=file_llm_service.extraction_prompt,
            summary_prompt=file_llm_service.summary_prompt,
            scoring_prompt=file_llm_service.scoring_prompt,
            thinking_regex=file_llm_service.thinking_regex,
            type=OPENAI_LLM_SERVICE_TYPE,
          )
        else:
          raise ValueError(f"Unknown llm service {file_llm_service.type}")

        pagination = PaginationSyncWorkerSiteConfig(
          template=site_file_config.pagination.template,
          start=site_file_config.pagination.start,
          stop=site_file_config.pagination.stop,
          step=site_file_config.pagination.step,
        )

        site_config = SyncWorkerSiteConfig(
          base_url=site_file_config.base_url,
          scraping_service=scraping_service,
          html_processor=html_processor,
          llm_service=llm_service,
          pagination=pagination,
        )

        site_configs[site_name] = site_config

      return SyncWorkerConfig(sites=site_configs, type=SYNC_WORKER_TYPE)

    raise ValueError(f"Unknown worker {config.file.worker.type}")

  @override
  def for_writer(self, config: Config) -> WriterConfig:
    return WriterConfig(
      config.args.output_path, config.args.output_format or Format.JSON
    )

  def _find_dynamic_config(
    self, explicit_path: Optional[str] = None
  ) -> Optional[str]:
    if explicit_path:
      path = explicit_path
      if self._system.path_exists(path):
        return path

    for ext in CONFIG_FILE_EXTENSIONS:
      path = f"{CONFIG_FILE_NAME}.{ext}"
      if self._system.path_exists(path):
        return path

    dynamic_config_dir = self._system.get_config_dir()

    for ext in CONFIG_FILE_EXTENSIONS:
      path = self._system.path_join(
        dynamic_config_dir, f"{CONFIG_FILE_NAME}.{ext}"
      )
      if self._system.path_exists(path):
        return path

    return None

  def _load_file_config(self, path: str) -> dict:
    format = self._system.takes_stdin()
    if format is not None:
      self._logger.debug(f"Reading config from stdin as {format.type}")
      config = format.deserialize(self._system.read_stdin())
    else:
      if not self._system.path_exists(path):
        return {}

      format = Format.from_suffix(self._system.path_suffix(path))
      config = format.deserialize(self._system.read_file(path))

    return self._check_and_convert_to_dict(config)

  def _read_if_path(self, maybe_path: str) -> str:
    if self._system.path_exists(maybe_path):
      return self._system.read_file(maybe_path)

    return maybe_path

  def _check_and_convert_to_dict(self, value: Any) -> dict:
    if not isinstance(value, dict):
      raise ValueError("Value is not a dictionary")

    return json.loads(json.dumps(value))
