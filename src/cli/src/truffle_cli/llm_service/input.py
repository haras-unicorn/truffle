from dataclasses import dataclass
from typing import Literal, Optional, Union

LlmServiceConfig = Union["OpenaiLlmServiceConfig"]


OPENAI_LLM_SERVICE_TYPE: Literal["openai"] = "openai"


@dataclass
class OpenaiLlmServiceConfig:
  base_url: str
  api_key: str
  model: str
  cv: str
  extraction_prompt: str
  summary_prompt: str
  scoring_prompt: str
  thinking_regex: Optional[str] = None
  type: Literal["openai"] = OPENAI_LLM_SERVICE_TYPE
