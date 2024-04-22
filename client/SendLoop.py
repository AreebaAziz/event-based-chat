from enum import Enum
import requests
import json
import logging

PORT = 3030

class EventType(Enum):
  SEND_MESSAGE = "sendMessage"
  DELETE_MESSAGE = "deleteMessage"
  EDIT_MESSAGE = "editMessage"

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

  if (userMsg.startswith("delete")):
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
          'id': id_to_delete
      }
    }
  elif (userMsg.startswith("edit")):
    # process edit message
    words = userMsg.split(" ")
    if len(words) < 3:
      print("You need to provide an ID of the message followed by the new message")
      return

    data = {
      'author': user,
      'action': EventType.EDIT_MESSAGE.value,
      'payload': {
          'id': words[1],
          'message': " ".join(words[2:])
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
