from enum import Enum
import requests
import json
import logging

PORT = 3030

class EventType(Enum):
  SEND_MESSAGE = "sendMessage"
  DELETE_MESSAGE = "deleteMessage"

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

  id_to_delete = None
  if (userMsg.startswith("delete")):
    try:
      id_to_delete = userMsg.split(" ")[1]
    except IndexError:
      print("Please provide a message ID to delete")

  if id_to_delete is None:
    # process sendMessage 
    data = {
      'author': user, 
      'action': EventType.SEND_MESSAGE.value, 
      'payload': {
        'message': userMsg
      }
    }
  else:
    # process delete message
    data = {
      'author': user,
      'action': EventType.DELETE_MESSAGE.value,
      'payload': {
          'id': id_to_delete
      }
    }
  response = requests.patch(url, data=json.dumps(data), headers=headers)

  logging.debug(f"Response Status Code: {response.status_code}")
  logging.debug(f"Response Content: {response.text}")
