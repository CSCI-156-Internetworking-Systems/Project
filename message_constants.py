import socket

print("Message Constants Imported!")

# message IDs that come from client:
REQ_GAME_LIST = 0
REQ_CREATE_GAME = 1
REQ_JOIN_GAME = 2

# response message IDs:
RES_NAME_TAKEN = 0
RES_GAME_CREATED = 1
RES_GAME_LIST = 2

def sendMSG(connection, id, data):
    connection.send(str.encode('{"msgId": %d, "data": "%s"}' % (id, data)))