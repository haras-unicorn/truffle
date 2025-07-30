from truffle_cli.system.abstract import System
from truffle_cli.system.platform import PlatformSystem


def create() -> System:
  return PlatformSystem()
