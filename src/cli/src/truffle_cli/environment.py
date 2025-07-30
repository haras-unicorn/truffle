from enum import Enum


class LogLevel(str, Enum):
  TRACE = "trace"
  DEBUG = "debug"
  INFO = "info"
  WARNING = "warning"
  ERROR = "error"
  CRITICAL = "critical"


class Environment(str, Enum):
  DEVELOPMENT = "development"
  PRODUCTION = "production"
