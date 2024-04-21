import logging
import sys
import Listener

if __name__ == "__main__":
  debug = True if len(sys.argv) > 1 and sys.argv[1] == '--debug' else False
  logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  logging.info("Listening for changes to event log")
  Listener.listen_for_changes()