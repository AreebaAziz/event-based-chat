from enum import Enum
import requests
import json
import logging

from common import colour_codes

PORT = 3030

class EventType(Enum):
  SEND_MESSAGE = "sendMessage"
  DELETE_MESSAGE = "deleteMessage"
  EDIT_MESSAGE = "editMessage"
  EVENT = "event"

class Commands(Enum):
  DELETE_CMD = "delete"
  EDIT_CMD = "edit"
  THEME_CMD = "theme"

def sendLoop(user: str):
  while True:
    userMsg = input("Enter your message: ")
    if (userMsg == "quit"):
      print("==== QUITTING ====")
      return
    sendMsgToServer(user, userMsg)

def sendMsgToServer(user: str, userMsg: str):
  url = f"http://localhost:{PORT}"
  headers = {'Content-Type': 'application/json'}

  if (userMsg.startswith(Commands.DELETE_CMD.value)):
    # process delete message
    id_to_delete = None
    try:
      id_to_delete = userMsg.split(" ")[1]
    except IndexError:
      print("Please provide a message ID to delete")
      return

    data = {
      'author': user,
      'action': EventType.DELETE_MESSAGE.value,
      'payload': {
          'id_to_delete': id_to_delete
      }
    }
  elif (userMsg.startswith(Commands.EDIT_CMD.value)):
    # process edit message
    words = userMsg.split(" ")
    if len(words) < 3:
      print("You need to provide an ID of the message followed by the new message")
      return

    data = {
      'author': user,
      'action': EventType.EDIT_MESSAGE.value,
      'payload': {
          'id_to_edit': words[1],
          'message': " ".join(words[2:])
      }
    }
  elif (userMsg.startswith(Commands.THEME_CMD.value)):
    # change the theme!
    words = userMsg.split(" ")
    if len(words) < 2 or words[1] not in colour_codes:
      print("You need to provide a valid colour for the theme!!")
      return
    data = {
      'author': user,
      'action': EventType.EVENT.value,
      'payload': {
        'flags': ['theme'],
        'props': {
          'colour': words[1]
        }
      }
    }
  else:
    # process sendMessage 
    data = {
      'author': user, 
      'action': EventType.SEND_MESSAGE.value, 
      'payload': {
        'message': userMsg
      }
    }

  response = requests.patch(url, data=json.dumps(data), headers=headers)

  logging.debug(f"Response Status Code: {response.status_code}")
  logging.debug(f"Response Content: {response.text}")
