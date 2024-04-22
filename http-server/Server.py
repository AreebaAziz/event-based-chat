import os
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import yaml
from datetime import datetime
import logging

EVENT_LOG_FILEPATH = "../event_log.yaml"
FIFO_QUEUE_FILEPATH = "../fifo_queue.yaml"

class FilePatchHandler(BaseHTTPRequestHandler):
  def do_PATCH(self):
    content_length = int(self.headers['Content-Length'])
    data = self.rfile.read(content_length)
    data = json.loads(data.decode('utf-8'))

    id = append_to_event_log(data)

    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()

    self.wfile.write(id.encode())

class QueuePatchHandler(BaseHTTPRequestHandler):
  def do_PATCH(self):
    content_length = int(self.headers['Content-Length'])
    data = self.rfile.read(content_length)
    data = json.loads(data.decode('utf-8'))

    id = enqueue_event(data)

    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()

    self.wfile.write(id.encode())

def run(port:int = 3030, write_to_event_log: bool = True):
  server_address = ('' , port)
  PatchHandler = FilePatchHandler if write_to_event_log else QueuePatchHandler
  httpd = HTTPServer(server_address, PatchHandler)
  logging.debug(f"Starting server on port {port}")
  httpd.serve_forever()

def append_to_event_log(data):
  logging.debug(f"Appending data to event log: {data}")

  # now we need to write to the event_log
  yaml_string, id = build_event(data)

  # append to event_log
  with open(EVENT_LOG_FILEPATH, 'a') as file:
    file.write(yaml_string)

  return id

def enqueue_event(data):
  logging.debug(f"Enqueuing event to fifo queue: {data}")
  yaml_string, id = build_event(data)

  # enqueue event 
  try:
    os.mkfifo(FIFO_QUEUE_FILEPATH)
  except FileExistsError:
    pass

  with open(FIFO_QUEUE_FILEPATH, 'w') as fifo:
    fifo.write(yaml_string)

  return id

def build_event(data: dict):
  timestamp = datetime.utcnow().timestamp()
  id = str(uuid.uuid4())[:7]
  event = [{'id': id, 'timestamp': timestamp, **data}]
  return yaml.dump(event), id
