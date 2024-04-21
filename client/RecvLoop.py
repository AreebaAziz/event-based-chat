import logging
import sys
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

GENERATED_CHAT_FILE = "../generated_chat.yaml"

def recvLoop():
  logging.debug("Starting recvLoop")
  listen_for_changes()
  while True:
    time.sleep(5) # we don't want this method to end until program ends (by other thread or ctrl+c)

def update_chat_ui():
  logging.debug("Will update UI")

class OnChangeHandler(FileSystemEventHandler):
  def on_any_event(self, event):
    logging.debug(f"File changed!")
    update_chat_ui()

def listen_for_changes():
  observer = Observer()
  observer.schedule(OnChangeHandler(), GENERATED_CHAT_FILE, recursive=True)
  observer.start()
