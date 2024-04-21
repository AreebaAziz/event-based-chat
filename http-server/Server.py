import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import yaml
from datetime import datetime
import logging

EVENT_LOG_FILEPATH = "../event_log.yaml"

class PatchHandler(BaseHTTPRequestHandler):
  def do_PATCH(self):
    content_length = int(self.headers['Content-Length'])
    data = self.rfile.read(content_length)
    data = json.loads(data.decode('utf-8'))

    id = appendToEventLog(data)

    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()

    self.wfile.write(id.encode())

def run(port:int = 3030):
  server_address = ('' , port)
  httpd = HTTPServer(server_address, PatchHandler)
  logging.debug(f"Starting server on port {port}")
  httpd.serve_forever()

def appendToEventLog(data):
  logging.debug(f"Appending data: {data}")

  # now we need to write to the event_log
  timestamp = datetime.utcnow().timestamp()
  id = str(uuid.uuid4())[:7]
  event = [{'id': id, 'timestamp': timestamp, **data}]
  yaml_string = yaml.dump(event)

  # append to event_log
  with open(EVENT_LOG_FILEPATH, 'a') as file:
    file.write(yaml_string)

  return id
