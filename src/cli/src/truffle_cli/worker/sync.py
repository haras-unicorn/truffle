import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Generator, override

import truffle_cli.html_processor as truffle_html_processor
import truffle_cli.http_client as truffle_http_client
import truffle_cli.llm_service as truffle_llm_service
import truffle_cli.scraping_service as truffle_scraping_service
from truffle_cli.html_processor.abstract import HtmlProcessor
from truffle_cli.llm_service.abstract import LlmService
from truffle_cli.logger.abstract import Logger
from truffle_cli.scraping_service.abstract import ScrapingService
from truffle_cli.system.abstract import System

from .abstract import Worker
from .input import SyncWorkerConfig, SyncWorkerSiteConfig
from .output import (
  OutputJob,
  OutputJobEnrichment,
  OutputJobScrape,
  OutputJobThinking,
  OutputMetadata,
)


@dataclass
class _SiteProcessingContext:
  name: str
  config: SyncWorkerSiteConfig
  scraping_service: ScrapingService
  html_processor: HtmlProcessor
  llm_service: LlmService


@dataclass
class _PageProcessingContext:
  site: _SiteProcessingContext
  page: int


@dataclass
class _LinkProcessingContext:
  page: _PageProcessingContext
  link: str


class SyncWorker(Worker):
  _system: System
  _config: SyncWorkerConfig
  _logger: Logger

  def __init__(self, system: System, config: SyncWorkerConfig):
    self._system = system
    self._config = config

    self._logger = self._system.get_logger(__name__)

  @override
  def run(self) -> Generator[OutputJob, None, OutputMetadata]:
    start = datetime.now(timezone.utc)

    self._logger.info(f"Starting: {start}")

    for name, site in self._config.sites.items():
      http_client = truffle_http_client.create(self._system)
      scraping_service = truffle_scraping_service.create(
        self._system, site.scraping_service, http_client
      )
      html_processor = truffle_html_processor.create(
        self._system, site.html_processor
      )
      llm_service = truffle_llm_service.create(
        self._system, site.llm_service, http_client
      )

      site_ctx = _SiteProcessingContext(
        name, site, scraping_service, html_processor, llm_service
      )

      yield from self._process_site(site_ctx)

    self._logger.info(f"Ending: {start}")

    end = datetime.now(timezone.utc)

    metadata = OutputMetadata(start, end)

    return metadata

  def _process_site(self, ctx: _SiteProcessingContext) -> Generator[OutputJob]:
    self._logger.info(f"Processing site: '{ctx.name}'")

    for page in range(
      ctx.config.pagination.start,
      ctx.config.pagination.stop,
      ctx.config.pagination.step,
    ):
      page_ctx = _PageProcessingContext(ctx, page)

      yield from self._process_page(page_ctx)

  def _process_page(
    self, ctx: _PageProcessingContext
  ) -> Generator[OutputJob, None, None]:
    page_url = str(ctx.site.config.pagination.template).format(ctx.page)

    self._logger.info(f"Processing page: '{page_url}'")

    try:
      page_html = ctx.site.scraping_service.list(page_url)
    except Exception as error:
      self._logger.err(
        f"Scraping page '{page_url}' failed - '{error}'. Skipping..."
      )
      return

    links = ctx.site.html_processor.links(page_html)

    for link in links:
      if link.startswith("/"):
        link = (
          str(ctx.site.config.base_url).removesuffix("/")
          + "/"
          + link.removeprefix("/")
        )

      link_ctx = _LinkProcessingContext(ctx, link)

      yield from self._process_link(link_ctx)

  def _process_link(
    self, ctx: _LinkProcessingContext
  ) -> Generator[OutputJob, None, None]:
    self._logger.info(f"Processing link: {ctx.link}")

    try:
      raw = ctx.page.site.scraping_service.details(ctx.link)
    except Exception as error:
      self._logger.err(
        f"Scraping link '{ctx.link}' failed - '{error}'. Skipping..."
      )
      return

    clean = ctx.page.site.html_processor.clean(raw)
    clean_content = clean

    title = ctx.page.site.html_processor.clean(
      ctx.page.site.html_processor.title(raw)
    )
    details = ctx.page.site.html_processor.clean(
      ctx.page.site.html_processor.details(raw)
    )

    try:
      extract = ctx.page.site.llm_service.extract(clean_content)
      extract_content = (
        f"Extracted data:\n{json.dumps(extract.reply, indent=True)}"
      )
    except Exception as error:
      self._logger.err(
        f"Extracting link '{ctx.link}' failed - '{error}'. Skipping..."
      )
      return

    try:
      summary = ctx.page.site.llm_service.summarize(
        clean_content, extract_content
      )
      summary_content = summary.reply
    except Exception as error:
      self._logger.err(
        f"Summarizing link '{ctx.link}' failed - '{error}'. Skipping..."
      )
      return

    try:
      score = ctx.page.site.llm_service.score(
        clean_content, extract_content, summary_content
      )
    except Exception as error:
      self._logger.err(
        f"Scoring link '{ctx.link}' failed - '{error}'. Skipping..."
      )
      return

    scrape = OutputJobScrape(raw, clean_content, title, details)
    enrichment = OutputJobEnrichment(extract.reply, summary.reply, score.reply)
    thinking = OutputJobThinking(
      extract.thinking, summary.thinking, score.thinking
    )
    output = OutputJob(
      ctx.page.site.name, ctx.link, scrape, enrichment, thinking
    )

    yield output
