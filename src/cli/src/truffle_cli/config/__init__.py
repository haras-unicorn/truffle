from truffle_cli.config.abstract import Loader
from truffle_cli.config.system import SystemLoader
from truffle_cli.system.abstract import System


def create(system: System) -> Loader:
  return SystemLoader(system)
