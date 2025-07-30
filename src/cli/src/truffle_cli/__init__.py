import truffle_cli.config as truffle_config
import truffle_cli.system as truffle_system
import truffle_cli.worker as truffle_worker
import truffle_cli.writer as truffle_writer
from truffle_cli.worker.output import OutputMetadata


def main():
  import sys

  system = truffle_system.create()
  loader = truffle_config.create(system)

  if system.needs_help():
    help = loader.help()
    print(help)
    sys.exit(0)

  if system.needs_schema():
    schema = loader.schema()
    print(schema)
    sys.exit(0)

  config = loader.load()
  if config is None:
    sys.exit(1)

  worker = truffle_worker.create(system, loader.for_worker(config))
  writer = truffle_writer.create(system, loader.for_writer(config))
  run = worker.run()
  try:
    while True:
      job = next(run)
      writer.write_job(job)
  except StopIteration as stop:
    if isinstance(stop.value, OutputMetadata):
      writer.write_metadata(stop.value)


if __name__ == "__main__":
  main()
