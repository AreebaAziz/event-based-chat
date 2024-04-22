import logging
import argparse
from QueueListener import QueueListener
from FileListener import FileListener

def doMain():
  parser = argparse.ArgumentParser(description="TrustedListener. Add debug or hardDelete option")
  parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help="Run with debug logging")
  parser.add_argument('--hardDelete', '-H', action=argparse.BooleanOptionalAction, help="Run with hard delete option. This will empty event log after processing every change")
  args = vars(parser.parse_args())

  debug = args['debug']
  hard_delete = args['hardDelete']
  logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  logging.info("Listening for changes to event log")
  
  if (hard_delete):
    listener = QueueListener()
  else:
    listener = FileListener()

  listener.listen_for_changes()

if __name__ == "__main__":
  doMain()