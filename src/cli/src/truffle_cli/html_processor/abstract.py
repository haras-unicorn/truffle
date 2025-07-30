from abc import ABC, abstractmethod
from typing import List


class HtmlProcessor(ABC):
  @abstractmethod
  def clean(self, html: str) -> str:
    pass

  @abstractmethod
  def title(self, html: str) -> str:
    pass

  @abstractmethod
  def details(self, html: str) -> str:
    pass

  @abstractmethod
  def links(self, html: str) -> List[str]:
    pass
