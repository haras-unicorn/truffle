from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, TypeVar

TReply = TypeVar("TReply")


@dataclass
class LlmReply[TReply]:
  reply: TReply
  thinking: Optional[str] = None


class LlmService(ABC):
  @abstractmethod
  def extract(self, *content: str) -> LlmReply[Any]:
    pass

  @abstractmethod
  def summarize(self, *content: str) -> LlmReply[str]:
    pass

  @abstractmethod
  def score(self, *content: str) -> LlmReply[float]:
    pass
