import logging
import sys
import argparse
import Server

PORT = 3030

def intro():
  print("===========================")
  print("Welcome to the chat demo (server)")
  print(f"Server will run on port {PORT}")
  print("===========================\n")

def main():
  intro()
  parser = argparse.ArgumentParser(
      description="HTTP Server. Add debug or hardDelete option. Ideally hardDelete should be retrieved from a chat channel.")
  parser.add_argument(
      '--debug', '-d', action=argparse.BooleanOptionalAction, help="Run with debug logging")
  parser.add_argument('--hardDelete', '-H', action=argparse.BooleanOptionalAction,
                      help="Run with hard delete option. This will empty event log after processing every change")
  args = vars(parser.parse_args())

  debug = args['debug']
  hard_delete = args['hardDelete']
  logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  Server.run(port=PORT, write_to_event_log=not hard_delete)

if __name__ == '__main__':
  main()
