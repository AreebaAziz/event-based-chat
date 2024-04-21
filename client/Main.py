import sys
import threading
import logging

from SendLoop import sendLoop
from RecvLoop import recvLoop

def intro(user: str):
  print("===========================")
  print("Welcome to the chat demo (client)")
  print(f"== You are {user} ==")
  print("===========================\n")


def main():
  if (len(sys.argv) < 2):
    print("ERROR - Must provide your username as an argument.")
    exit(1)
  user = sys.argv[1]
  intro(user)
  debug = True if len(sys.argv) > 2 and sys.argv[2] == '--debug' else False
  logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  sendThread = threading.Thread(target=sendLoop, args=(user,))
  recvThread = threading.Thread(target=recvLoop, daemon=True)
  sendThread.start()
  recvThread.start()
  sendThread.join()

if __name__ == '__main__':
  main()
