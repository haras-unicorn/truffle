from truffle_cli.system.abstract import System

from .abstract import HtmlProcessor
from .beautiful_soup import BeautifulSoupHtmlProcessor
from .input import BEAUTIFUL_SOUP_HTML_PROCESSOR_TYPE, HtmlProcessorConfig


def create(system: System, config: HtmlProcessorConfig) -> HtmlProcessor:
  if config.type == BEAUTIFUL_SOUP_HTML_PROCESSOR_TYPE:
    return BeautifulSoupHtmlProcessor(system, config)
