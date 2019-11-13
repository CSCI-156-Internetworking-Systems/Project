import socket
import json
from enum import IntEnum, unique

print("Message Constants Imported!")

class MessageID(IntEnum):
    pass

# message IDs that come from client:
@unique
class RequestMessageID(MessageID):
    LIST_GAMES = 0
    CREATE_GAME = 1
    JOIN_GAME = 2

# response message IDs:
@unique
class ResponseMessageID(MessageID):
    NAME_TAKEN = 0
    GAME_CREATED = 1
    GAME_LIST = 2

class Message:
    def __init__(self, message_id: MessageID, body: str):
        self.__message_id = message_id
        self.__body       = body

# connection - some socket object for the message to be sent through
# id - the ID of the message to tell the receiver what the message is about, i.e. what to do with the data
# data - some object, such as a string or array
def sendMSG(connection, id, data):
    outJSON = {"id": id, "data": data}
    connection.send(str.encode(json.dumps(outJSON)))