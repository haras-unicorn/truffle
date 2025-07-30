from html import unescape
from typing import List, override

from bs4 import BeautifulSoup, Comment

from truffle_cli.logger.abstract import Logger
from truffle_cli.system.abstract import System

from .abstract import HtmlProcessor
from .input import BeautifulSoupHtmlProcessorConfig


class BeautifulSoupHtmlProcessor(HtmlProcessor):
  _config: BeautifulSoupHtmlProcessorConfig
  _system: System
  _logger: Logger

  def __init__(self, system: System, config: BeautifulSoupHtmlProcessorConfig):
    self._config = config
    self._system = system

    self._logger = self._system.get_logger(__name__)

  @override
  def title(self, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    title = str(soup.select_one(self._config.title_selector))

    self._logger.debug(f"Title:\n{title}")

    return title

  @override
  def details(self, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    content = str(soup.select_one(self._config.details_selector))

    self._logger.debug(f"Content:\n{content}")

    return content

  @override
  def links(self, html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")

    elements = soup.select(self._config.link_selector)

    links = []
    for element in elements:
      href = element.get("href")
      if href:
        links.append(href)

    self._logger.debug("Links:\n" + "\n".join(links))

    return links

  @override
  def clean(self, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    disallowed_tags = ["script", "style", "nav", "header", "footer", "aside"]
    for element in soup(disallowed_tags):
      element.decompose()

    disallowed_selectors = [
      '[class*="ad-"]',
      '[class*="advertisement"]',
      '[class*="tracking"]',
      '[class*="cookie"]',
      '[class*="popup"]',
      '[class*="modal"]',
      '[id*="google"]',
      '[class*="google"]',
    ]
    for selector in disallowed_selectors:
      for element in soup.select(selector):
        element.decompose()

    allowed_tags = [
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6",
      "p",
      "div",
      "span",
      "ul",
      "ol",
      "li",
      "strong",
      "b",
      "em",
      "i",
    ]
    for tag in soup.find_all():
      if tag.name not in allowed_tags:  # type: ignore
        tag.unwrap()  # type: ignore

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
      comment.extract()

    for tag in soup.find_all():
      if tag.get_text(strip=True) == "":
        tag.decompose()

    allowed_attrs = ["id", "title", "alt", "href"]
    for tag in soup.find_all():
      if hasattr(tag, "attrs"):
        tag.attrs = {  # type: ignore
          k: v
          for k, v in tag.attrs.items()  # type: ignore
          if k in allowed_attrs  # type: ignore
        }

    text = str(soup)

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = " ".join(chunk for chunk in chunks if chunk)

    clean = unescape(text)

    self._logger.debug(f"Cleaned: {clean}")

    return clean
