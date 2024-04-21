import logging
import sys
import argparse
import Listener

def doMain():
  # debug = True if len(sys.argv) > 1 and sys.argv[1] == '--debug' else False
  parser = argparse.ArgumentParser(description="TrustedListener. Add debug or hardDelete option")
  parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction, help="Run with debug logging")
  parser.add_argument('--hardDelete', '-H', action=argparse.BooleanOptionalAction, help="Run with hard delete option. This will empty event log after processing every change")
  args = vars(parser.parse_args())

  debug = args['debug']
  hard_delete = args['hardDelete']
  logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  logging.info("Listening for changes to event log")
  Listener.listen_for_changes(hard_delete=hard_delete)

if __name__ == "__main__":
  doMain()