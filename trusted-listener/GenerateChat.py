import yaml
import logging
from enum import Enum

EVENT_LOG_FILE = "../event_log.yaml"
GENERATED_CHAT_FILE = "../generated_chat.yaml"

class Flags(Enum):
  DELETED_MESSAGE = 'deleted'

class EventType(Enum):
  SEND_MESSAGE = "sendMessage"
  DELETE_MESSAGE = "deleteMessage"

class Message:
  def __init__(self, id: str, timestamp: str, author: str):
    self.id = id
    self.author = author
    self.timestamp = timestamp
    self.contents = None
    self.props = {}
    self.flags = []
  
  @classmethod
  def from_genchat(cls, data):
    # figure out which is the best subclass to associate with this data
    # first we check flags to see if there are hints for known subclasses
    if len(data['flags']) == 0:
      # if no flags, then we can use SimpleMessage. Props will be ignored if there 
      # are no flags. 
      pass
    elif Flags.DELETED_MESSAGE.value in data['flags']:
      return DeletedMessage(data['id'], data['timestamp'], data['author'])
    
    # if we see no known flags, we can interprete the message as a SimpleMessage
    return SimpleMessage(data['id'], data['timestamp'], data['author'], data['contents'])

class SimpleMessage(Message):
  def __init__(self, id: str, timestamp: str, author: str, message: str):
    super().__init__(id, timestamp, author)
    self.contents = message
  
  @classmethod
  def from_event(cls, data):
    return cls(data['id'], data['timestamp'], data['author'], data['payload']['message'])

  @classmethod
  def from_genchat(cls, data):
    return cls(data['id'], data['timestamp'], data['author'], data['contents'])

class DeletedMessage(SimpleMessage):
  def __init__(self, id: str, timestamp: str, author: str):
    super().__init__(id, timestamp, author, "(deleted)")
  
  @classmethod
  def from_event(cls, data):
    return cls(data['id'], data['timestamp'], data['author'])

  @classmethod
  def from_genchat(cls, data):
    return cls(data['id'], data['timestamp'], data['author'])

def generate_chat(hard_delete:bool = False):
  logging.debug("Generating chat based on events")

  generated_msgs: list[Message] = []
  if (not hard_delete):
    generated_msgs = apply_incremental_event_log_changes()
  else:
    generated_msgs = apply_change_to_shallow_copy()

  if generated_msgs is None:
    return

  # now we have a generated list of processed messages.
  # we can now use this generated list to write to the generated_chat file
  data = [vars(msg) for msg in generated_msgs]
  yaml_string = yaml.dump(data)

  # write to generated_chat
  with open(GENERATED_CHAT_FILE, 'w') as file:
    file.write(yaml_string)

  logging.info("Generated chat after file changed")

def apply_incremental_event_log_changes() -> list[Message]:
  # first read the entire event log file in yaml
  with open(EVENT_LOG_FILE, 'r') as file:
    events = yaml.safe_load(file)

  generated_msgs: list[Message] = []
  # go through each event and process accordingly
  for event in events:
    logging.debug('EVENT------ ')
    logging.debug(event)
    if (event['action'] == EventType.SEND_MESSAGE.value):
      logging.debug("Processing sendMessage event")
      # in case of sendMessage event, we just append this event to the list of messages
      generated_msgs.append(SimpleMessage.from_event(event))
    elif (event['action'] == EventType.DELETE_MESSAGE.value):
      logging.debug("Processing deleteMessage event")
      # in case of delete message, we must go through the generatedMsgs list and remove the item
      # with the provided id
      id_to_delete = event['payload']['id']
      # the deleted msg must already exist in the list as it must have come before this current event
      generated_msgs = [
          msg if not (msg.id == id_to_delete and msg.author == event['author']) 
                  else DeletedMessage.from_event(event)
          for msg in generated_msgs
      ]

  return generated_msgs

def apply_change_to_shallow_copy() -> list[Message]:
  # read the generated chat file instead and compute how the latest event changes the 
  # generated chat
  
  # for the demo implementation we will read the latest event from the event_log file.
  # In a better implementation/design, we will receive the latest event from the HTTP server
  # directly on a PATCH request. 

  with open(EVENT_LOG_FILE, 'r') as file:
    events = yaml.safe_load(file)
  
  if events is None:
    # this file change event was likely triggered after we cleared the event_log file from after previous event
    return None
  latest_event = events[-1]

  # read the generated_chat file to get the current state of the chat
  with open(GENERATED_CHAT_FILE, 'r') as file:
    msgs_from_file = yaml.safe_load(file)
  
  # process into subclass of Message
  generated_msgs = []
  if msgs_from_file is not None:
    generated_msgs = [Message.from_genchat(msg) for msg in msgs_from_file]

  if (latest_event['action'] == EventType.SEND_MESSAGE.value):
    logging.debug("Processing sendMessage event")
    # in case of sendMessage event, we just append this event to the list of messages
    generated_msgs.append(SimpleMessage.from_event(latest_event))
  elif (latest_event['action'] == EventType.DELETE_MESSAGE.value):
    logging.debug("Processing deleteMessage event")
    # in case of delete message, we must go through the generatedMsgs list and remove the item
    # with the provided id
    id_to_delete = latest_event['payload']['id']
    # the deleted msg must already exist in the generated_msgs list
    generated_msgs = [
          msg if not (msg.id == id_to_delete and msg.author == latest_event['author']) 
                  else DeletedMessage.from_event(latest_event)
          for msg in generated_msgs
      ]
  
  return generated_msgs
