from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Literal, Optional, Union


# NOTE: this is just for reference
# the output list will always start with jobs
# only the last object will be metadata
# this is to optimize memory usage and only append to output file
@dataclass
class Output:
  output: List[Union["OutputJob", "OutputMetadata"]]


@dataclass
class OutputMetadata:
  start: datetime
  end: datetime
  type: Literal["metadata"] = "metadata"


@dataclass
class OutputJob:
  site: str
  link: str
  scrape: "OutputJobScrape"
  enrichment: "OutputJobEnrichment"
  thinking: "OutputJobThinking"
  type: Literal["job"] = "job"


@dataclass
class OutputJobScrape:
  raw: str
  clean: str
  title: str
  content: str


@dataclass
class OutputJobEnrichment:
  extract: Any
  summary: str
  score: float


@dataclass
class OutputJobThinking:
  extract: Optional[str]
  summary: Optional[str]
  score: Optional[str]
