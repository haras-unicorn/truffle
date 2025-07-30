from truffle_cli.http_client.abstract import HttpClient
from truffle_cli.system.abstract import System

from .abstract import LlmService
from .input import OPENAI_LLM_SERVICE_TYPE, LlmServiceConfig
from .openai import OpenaiLlmService


def create(
  system: System, config: LlmServiceConfig, client: HttpClient
) -> LlmService:
  if config.type == OPENAI_LLM_SERVICE_TYPE:
    return OpenaiLlmService(system, config, client)
