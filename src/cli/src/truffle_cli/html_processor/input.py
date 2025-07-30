from dataclasses import dataclass
from typing import Literal, Union

HtmlProcessorConfig = Union["BeautifulSoupHtmlProcessorConfig"]


BEAUTIFUL_SOUP_HTML_PROCESSOR_TYPE: Literal["beautiful-soup"] = "beautiful-soup"


@dataclass
class BeautifulSoupHtmlProcessorConfig:
  link_selector: str
  title_selector: str
  details_selector: str
  type: Literal["beautiful-soup"] = BEAUTIFUL_SOUP_HTML_PROCESSOR_TYPE
