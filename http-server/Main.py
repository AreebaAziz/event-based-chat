import logging
import sys
import Server

PORT = 3030

def intro():
  print("===========================")
  print("Welcome to the chat demo (server)")
  print(f"Server will run on port {PORT}")
  print("===========================\n")

def main():
  intro()
  debug = True if len(sys.argv) > 1 and sys.argv[1] == '--debug' else False
  logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                      format='%(asctime)s - %(levelname)s - %(message)s')
  Server.run(port=PORT)

if __name__ == '__main__':
  main()
