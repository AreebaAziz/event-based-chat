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
  data = {
    'author': user, 
    'action': EventType.SEND_MESSAGE.value, 
    'body': {
      'message': userMsg
    }
  }
  response = requests.patch(url, data=json.dumps(data), headers=headers)

  logging.debug(f"Response Status Code: {response.status_code}")
  logging.debug(f"Response Content: {response.text}")
