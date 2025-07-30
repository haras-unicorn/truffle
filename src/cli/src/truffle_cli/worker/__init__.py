from truffle_cli.system.abstract import System

from .abstract import Worker
from .input import WorkerConfig
from .sync import SyncWorker


def create(system: System, config: WorkerConfig) -> Worker:
  if config.type == "sync":
    return SyncWorker(system, config)
