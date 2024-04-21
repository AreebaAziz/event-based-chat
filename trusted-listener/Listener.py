import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from GenerateChat import generate_chat

EVENT_LOG_FILE = "../event_log.yaml"

class EventHandler(FileSystemEventHandler):
  def on_any_event(self, event):
    logging.debug(f"File changed!")
    generate_chat()

def listen_for_changes():
  observer = Observer()
  observer.schedule(EventHandler(), EVENT_LOG_FILE, recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
