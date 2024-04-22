import yaml
import logging
from Models import *

EVENT_LOG_FILE = "../event_log.yaml"
GENERATED_CHAT_FILE = "../generated_chat.yaml"

def generate_chat(from_event_log: bool = True, events: list[dict] = []):
  logging.debug("Generating chat based on events")

  generated_msgs: list[Message] = []
  if from_event_log:
    generated_msgs = apply_incremental_event_log_changes()
  else:
    generated_msgs = apply_change_to_shallow_copy(events)

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

def apply_change_to_shallow_copy(events: list[dict]) -> list[Message]:
  # read the generated chat file instead and compute how the latest event changes the 
  # generated chat

  # read the generated_chat file to get the current state of the chat
  with open(GENERATED_CHAT_FILE, 'r') as file:
    msgs_from_file = yaml.safe_load(file)
  
  # process into subclass of Message
  generated_msgs = []
  if msgs_from_file is not None:
    generated_msgs = [Message.from_genchat(msg) for msg in msgs_from_file]

  for event in events:
    if (event['action'] == EventType.SEND_MESSAGE.value):
      logging.debug("Processing sendMessage event")
      # in case of sendMessage event, we just append this event to the list of messages
      generated_msgs.append(SimpleMessage.from_event(event))
    elif (event['action'] == EventType.DELETE_MESSAGE.value):
      logging.debug("Processing deleteMessage event")
      # in case of delete message, we must go through the generatedMsgs list and remove the item
      # with the provided id
      id_to_delete = event['payload']['id']
      # the deleted msg must already exist in the generated_msgs list
      generated_msgs = [
            msg if not (msg.id == id_to_delete and msg.author == event['author']) 
                    else DeletedMessage.from_event(event)
            for msg in generated_msgs
        ]
  
  return generated_msgs
