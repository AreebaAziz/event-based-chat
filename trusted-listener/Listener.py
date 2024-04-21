import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver
from GenerateChat import generate_chat

EVENT_LOG_FILE = "../event_log.yaml"

class EventHandler(FileSystemEventHandler):
  def __init__(self, hard_delete: bool = False):
    self.hard_delete = hard_delete

  def on_any_event(self, event):
    logging.debug(f"File changed!")
    generate_chat(hard_delete=self.hard_delete)
    if self.hard_delete:
      clear_event_log()

def listen_for_changes(hard_delete: bool = False):
  observer = PollingObserver()
  observer.schedule(EventHandler(hard_delete), EVENT_LOG_FILE, recursive=True)
  observer.start()
  print("observer started")
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  print("just before join")
  observer.join()

def clear_event_log():
  '''
    Here we are actually giving write permissions to the Trusted Listener, but it should only 
    have read permissions to the event log file. 
    There could be other implementations that don't require Write permissions. For example, the 
    Trusted Listener could intercept the HTTP PATCH request and not even write anything to 
    the event log file. It would process only this latest event from the PATCH request, read the 
    current generated_chat file and compute the change into a new version of the generated file.
  '''
  with open(EVENT_LOG_FILE, 'w') as file:
    file.write("")
