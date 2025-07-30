from truffle_cli.http_client.abstract import HttpClient
from truffle_cli.http_client.requests import RequestsHttpClient
from truffle_cli.system.abstract import System


def create(system: System) -> HttpClient:
  return RequestsHttpClient(system)
