import socket
import json

print("Message Constants Imported!")

# message IDs that come from client:
REQ_GAME_LIST = 0
REQ_CREATE_GAME = 1
REQ_JOIN_GAME = 2

# response message IDs:
RES_NAME_TAKEN = 0
RES_GAME_CREATED = 1
RES_GAME_LIST = 2

# connection - some socket object for the message to be sent through
# id - the ID of the message to tell the receiver what the message is about, i.e. what to do with the data
# data - some object, such as a string or array
def sendMSG(connection, id, data):
    outJSON = {"id": id, "data": data}
    connection.send(str.encode(json.dumps(outJSON)))