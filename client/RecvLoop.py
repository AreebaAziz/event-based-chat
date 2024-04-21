import logging
import sys
import os
import time
import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

GENERATED_CHAT_FILE = "../generated_chat.yaml"

def recvLoop(user: str):
  logging.debug("Starting recvLoop")
  update_chat_ui(user)
  listen_for_changes(user)

def update_chat_ui(user: str):
  logging.debug("Will update UI")
  # first read the generated chat log file in yaml
  with open(GENERATED_CHAT_FILE, 'r') as file:
    messages = yaml.safe_load(file)
  
  # update UI
  clear()
  print("\n====== CHAT BEGIN =======")
  if messages is not None:
    for msg in messages:
      if len(msg['flags']) == 0: # regular messages will be stored in contents. All other event types, their properties would be in props, and content may be ignored
        iamAuthor = user == msg['author']
        print(f"{'Me' if iamAuthor else msg['author']}{' [' + msg['id'] + ']' if True else ''}: {msg['contents']}")
        
  print("====== CHAT END =======")
  print("Enter your message: ", end="", flush=True)

class OnChangeHandler(FileSystemEventHandler):
  def __init__(self, user: str):
    super().__init__()
    self.user = user

  def on_any_event(self, event):
    logging.debug(f"File changed!")
    update_chat_ui(self.user)

def listen_for_changes(user: str):
  observer = PollingObserver()
  observer.schedule(OnChangeHandler(user), GENERATED_CHAT_FILE, recursive=True)
  observer.start()
  while True:
    # we don't want this method to end until program ends (by other thread or ctrl+c)
    time.sleep(5)

def clear():
    os.system('clear')
