from abc import ABC, abstractmethod


class ScrapingService(ABC):
  @abstractmethod
  def list(self, url: str) -> str:
    pass

  @abstractmethod
  def details(self, url: str) -> str:
    pass
