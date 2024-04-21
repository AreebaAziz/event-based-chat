import yaml
import logging
from enum import Enum

EVENT_LOG_FILE = "../event_log.yaml"
GENERATED_CHAT_FILE = "../generated_chat.yaml"

class EventType(Enum):
  SEND_MESSAGE = "sendMessage"
  DELETE_MESSAGE = "deleteMessage"

class Message:
  def __init__(self, author: str, timestamp: str):
    self.author = author
    self.timestamp = timestamp
    self.contents = None
    self.props = None

class SimpleMessage(Message):
  def __init__(self, author: str, timestamp: str, message: str):
    super().__init__(author, timestamp)
    self.contents = message

def generate_chat():
  logging.debug("Generating chat based on events")
  generated_msgs = []

  # first read the entire event log file in yaml
  with open(EVENT_LOG_FILE, 'r') as file:
    events = yaml.safe_load(file)

  # go through each event and process accordingly
  for event in events:
    logging.debug('EVENT------ ')
    logging.debug(event)
    if (event['action'] == EventType.SEND_MESSAGE.value):
      logging.debug("Processing sendMessage event")
      # in case of sendMessage event, we just append this event to the list of messages
      generated_msgs.append(SimpleMessage(event['action'], event['timestamp'], event['body']['message']))

  # now we have a generated list of processed messages. 
  # we can now use this generated list to write to the generated_chat file
  data = [vars(msg) for msg in generated_msgs]
  yaml_string = yaml.dump(data)

  # write to generated_chat
  with open(GENERATED_CHAT_FILE, 'w') as file:
    file.write(yaml_string)
  
  logging.info("Generated chat after file changed")
