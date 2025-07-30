from abc import ABC, abstractmethod
from typing import Any, Dict


class HttpClient(ABC):
  @abstractmethod
  def post(self, url: str, headers: Dict[str, str], payload: Any) -> Any:
    pass
