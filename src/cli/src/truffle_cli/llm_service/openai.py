import json
import math
import re
from typing import Any, Final, override

from truffle_cli.http_client import HttpClient
from truffle_cli.logger.abstract import Logger
from truffle_cli.system.abstract import System

from .abstract import LlmReply, LlmService
from .input import OpenaiLlmServiceConfig

EXTRACTION_SYSTEM_PROMPT: Final[str] = """
You are an assistant that extracts data job posts based on the users' CV's and requirements.
You ONLY provide responses in JSON format.
You follow the user-provided JSON schema.
Do NOT provide responses in any format other than JSON.
Do NOT provide any other additional information.
""".strip()

SUMMARIZATION_SYSTEM_PROMPT: Final[str] = """
You are an assistant that summarizes job posts based on the users' CV's and requirements.
You ONLY provide responses in Markdown format.
Do NOT provide responses in any other format.
""".strip()

SCORING_SYSTEM_PROMPT: Final[str] = """
You are an assistant that scores job posts based on the users' CV's and requirements.
You ONLY provide a finite floating point number response.
You ALWAYS provide a number on a scale from 0 to 100.
Do NOT provide any other explanation, analysis or additional information.
""".strip()


class OpenaiLlmService(LlmService):
  _config: OpenaiLlmServiceConfig
  _client: HttpClient
  _system: System
  _logger: Logger

  def __init__(
    self, system: System, config: OpenaiLlmServiceConfig, client: HttpClient
  ):
    self._config = config
    self._client = client
    self._system = system

    self._logger = self._system.get_logger(__name__)

  @override
  def extract(self, *content: str) -> LlmReply[Any]:
    response = self._call(
      EXTRACTION_SYSTEM_PROMPT, self._config.extraction_prompt, *content
    )

    text = response.reply.strip("`").strip("```").strip("json").strip()
    reply = json.loads(text)
    thinking = response.thinking

    self._logger.debug(f"Extracted:\n{json.dumps(reply, indent=True)}")

    return LlmReply(reply, thinking)

  @override
  def summarize(self, *content: str) -> LlmReply[str]:
    response = self._call(
      SUMMARIZATION_SYSTEM_PROMPT, self._config.summary_prompt, *content
    )

    text = response.reply.strip("`").strip("```").strip("markdown").strip()
    reply = text
    thinking = response.thinking

    self._logger.debug(f"Summarized:\n{reply}")

    return LlmReply(reply, thinking)

  @override
  def score(self, *content: str) -> LlmReply[float]:
    response = self._call(
      SCORING_SYSTEM_PROMPT, self._config.scoring_prompt, *content
    )

    reply = float(response.reply)
    thinking = response.thinking

    if not math.isfinite(reply):
      raise ValueError(f"Llm score is not a finite number - {response}")

    self._logger.debug(f"Scored: {reply}")

    return LlmReply(reply, thinking)

  def _call(
    self, system_prompt: str, user_prompt: str, *content: str
  ) -> LlmReply[str]:
    payload = {
      "model": self._config.model,
      "messages": [
        {"role": "system", "content": system_prompt},
        {
          "role": "user",
          "content": f"The following is the user's CV.\n======\n{self._config.cv}",
        },
        {
          "role": "user",
          "content": f"The following is the user's requirements.\n======\n{user_prompt}",
        },
        *[
          {
            "role": "user",
            "content": f"The following is the job post content.\n\n======\n{content}",
          }
          for content in content
        ],
      ],
      "stream": False,
    }

    headers = {
      "Authorization": f"Bearer {self._config.api_key}",
      "Content-Type": "application/json",
    }

    url = f"{self._config.base_url}/chat/completions"
    response = self._client.post(url, headers, payload)
    reply: str = response["choices"][0]["message"]["content"].strip()

    thinking = None
    if self._config.thinking_regex is not None:
      reply = re.sub(self._config.thinking_regex, "", response)

      match = re.match(self._config.thinking_regex, response)
      if match is not None:
        thinking = match.string

    return LlmReply(reply, thinking)
