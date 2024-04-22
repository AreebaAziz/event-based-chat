# Note this should mimic a queue such as by using FIFO named pipe on unix
# but I couldn't get it to be stable in a time of 2 hours so I am just
# using a file listener on a queue file to mimic a queue. 
# This should actually be implemented as a queue where http server writes
# to this queue and the trusted listener listens for items in the queue
# for processing. In reality it could be implemented in many ways. Eg. named pipes, sockets, SQS queue in a larger system, etc

import logging
import time
import sys
from datetime import datetime
import yaml
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from Models import Listener
from GenerateChat import generate_chat

FIFO_QUEUE_FILEPATH = "../fifo_queue.yaml"

class QueueListener(Listener):
  def listen_for_changes(self):
    observer = PollingObserver()
    observer.schedule(EventHandler(self.process_change),
                      FIFO_QUEUE_FILEPATH, recursive=True)
    observer.start()
    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      observer.stop()
    observer.join()

  def process_change(self):
    print("process change triggered ", datetime.utcnow())
    events = []
    with open(FIFO_QUEUE_FILEPATH, 'r+') as file:
      events = yaml.safe_load(file)
      if events is not None:
        file.truncate(0) # "dequeue"
        generate_chat(from_event_log=False, events=events)

class EventHandler(FileSystemEventHandler):
  def __init__(self, process_change_fn):
    self.process_change_fn = process_change_fn

  def on_any_event(self, event):
    logging.debug(f"File changed!")
    self.process_change_fn()

# import os
# import yaml
# import time
# from watchdog.observers.polling import PollingObserver
# from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer

# from Models import Listener
# from GenerateChat import generate_chat

# FIFO_QUEUE_FILEPATH = "../fifo_queue.yaml"

# class QueueListener(Listener):
#   def listen_for_changes(self):
#     try:
#       os.mkfifo(FIFO_QUEUE_FILEPATH)
#     except FileExistsError:
#       pass

#     with open(FIFO_QUEUE_FILEPATH, 'r+') as fifo:
#       print("FIFO opened")
#       lines = ""
#       while True:
#         curr_line = fifo.readline()
#         if not curr_line:
#           # fifo.truncate(0)
#           lines = ""
#         elif curr_line == "EOF":
#           data = yaml.safe_load(lines)
#           print("processing a new event")
#           self.process_change(data[0])
#         else:
#           lines += curr_line
#         # events = yaml.safe_load(fifo)
#         # if events is not None:  
#         #   print("EVENTS")
#         #   print(events)
#         #   for event in events:
#         #     print("processing a change")
#         #     self.process_change(event)
#         #   fifo.write("")
#         # print("end of a loop")
#         # time.sleep(1)

#   def process_change(self, event: dict):
#     print("EVENT")
#     print(event)
#     generate_chat(from_event_log=False, event=event)
