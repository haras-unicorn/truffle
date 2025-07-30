from dataclasses import dataclass
from typing import Any, Dict, List, override

from truffle_cli.http_client.abstract import HttpClient


@dataclass
class TestRequest:
  __test__ = False

  url: str
  headers: Dict[str, str]
  payload: Any


class TestHttpClient(HttpClient):
  __test__ = False

  requests: List[TestRequest]

  def __init__(self):
    self.requests = []

  @override
  def post(self, url: str, headers: Dict[str, str], payload: Any) -> Any:
    self.requests.append(TestRequest(url, headers, payload))

    return {}
