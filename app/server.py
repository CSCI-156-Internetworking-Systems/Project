import socket
import threading
import json
from message import (
    RequestMessageID, ResponseMessageID, Message, MessageEncoder, MessageDecoder, sendMSG)

# list of all connected players waiting for a second player to join them:
gameList = {} 

class ClientThread(threading.Thread):

    def __init__(self, clientConnection):
        threading.Thread.__init__(self)
        self.connection = clientConnection
        self.requestHandlers = {
            RequestMessageID.JOIN_SERVER:  self.onRequestJoinServer,
            RequestMessageID.GET_AVAILABLE_GAMES:  self.onRequestAvailbaleGames
        }

    def run(self):
        while True:
            data = self.connection.recv(4096)
            if not data:
                break
            request = json.loads(data.decode("utf-8"), cls=MessageDecoder)
            print("---Client Message---")
            print(request)
            print("--------------------")
            self.requestHandlers[request['id']](request['body'])

    def onRequestJoinServer(self, requestParams):
        response = {}
        print('gameList', gameList)
        try:
            nickname = requestParams['nickname']
            p2pPort  = requestParams['p2pPort']
        except KeyError as error:
            response['id'] = ResponseMessageID.JOIN_SERVER_ERROR
            response['body'] = { 'error': str(error) }
        else:
            if nickname in gameList:
                response['id'] = ResponseMessageID.JOIN_SERVER_ERROR
                response['body'] = { 'error': 'Nickname already exists' }
            else:
                gameList[nickname] = p2pPort
                response['id'] = ResponseMessageID.JOIN_SERVER_SUCCESS
                response['body'] = None

        response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
        self.connection.send(response)


    def onRequestAvailbaleGames(self, requestParams):
        response = {}
        try:
            requesterNickname = requestParams['nickname']
            print(requesterNickname)
        except KeyError as error:
            response['id']   = ResponseMessageID.GET_AVAILABLE_GAMES_ERROR
            response['body'] = { 'error': str(error) }
        else:
            availableGames = [{'nickname': nickname, 'p2pPort': p2pPort}
                            for nickname, p2pPort in gameList.items()
                            if nickname != requesterNickname] 
            response['id'] = ResponseMessageID.GET_AVAILABLE_GAMES_SUCCESS
            response['body'] = { 'availableGames': availableGames }

        response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
        self.connection.send(response)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8080))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    connection, address = server.accept()
    print('recieved request...')
    requestHandlerThread = ClientThread(connection)
    print('created thread to handle request...')
    requestHandlerThread.start()
    print('handling request in separate thread')
