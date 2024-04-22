import logging
import time
import sys
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from Models import Listener
from GenerateChat import generate_chat

EVENT_LOG_FILE = "../event_log.yaml"

class FileListener(Listener):
  def listen_for_changes(self):
    observer = PollingObserver()
    observer.schedule(EventHandler(self.process_change), EVENT_LOG_FILE, recursive=True)
    observer.start()
    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      observer.stop()
    observer.join()

  def process_change(self):
      generate_chat(from_event_log=True)

class EventHandler(FileSystemEventHandler):
  def __init__(self, process_change_fn):
    self.process_change_fn = process_change_fn

  def on_any_event(self, event):
    logging.debug(f"File changed!")
    self.process_change_fn()
