from enum import Enum

class Flags(Enum):
  DELETED_MESSAGE = 'deleted'

class EventType(Enum):
  SEND_MESSAGE = "sendMessage"
  DELETE_MESSAGE = "deleteMessage"
  EDIT_MESSAGE = "editMessage"

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
    self.flags.append("deleted")

  @classmethod
  def from_event(cls, data):
    return cls(data['id'], data['timestamp'], data['author'])

  @classmethod
  def from_genchat(cls, data):
    return cls(data['id'], data['timestamp'], data['author'])

class EditedMessage(SimpleMessage):
  def __init__(self, id: str, timestamp: str, author: str, message: str):
    super().__init__(id, timestamp, author, message + " (edited)")
    self.flags.append("edited")

  @classmethod
  def from_event(cls, data):
    return cls(data['id'], data['timestamp'], data['author'], data['payload']['message'])

  @classmethod
  def from_genchat(cls, data):
    return cls(data['id'], data['timestamp'], data['author'])

class Listener:
  def listen_for_changes(self):
    raise NotImplementedError("Not implemented")
  
  def process_change(self):
    raise NotImplementedError("Not implemented")