import socket
import threading
import json
import random
from message import (
    RequestMessageID, ResponseMessageID, Message, MessageEncoder, MessageDecoder, sendMSG)
from game_logic import TicTacToe

# list of all connected players waiting for a second player to join them:
gameList = {}
gameBoards = {}

class ClientThread(threading.Thread):

    def __init__(self, clientConnection, clientAddress):
        threading.Thread.__init__(self)
        self.connection = clientConnection
        self.ipAddress  = clientAddress[0]

        self.requestHandlers = {
            RequestMessageID.JOIN_SERVER:  self.onRequestJoinServer,
            RequestMessageID.GET_AVAILABLE_GAMES:  self.onRequestAvailbaleGames,
            RequestMessageID.JOIN_GAME: self.onRequestJoinGame,
            RequestMessageID.MAKE_MOVE: self.onRequestMakeMove,
            RequestMessageID.GET_MOVE: self.onRequestGetMove,
            RequestMessageID.END_GAME: self.onRequestEndGame,
            RequestMessageID.LEAVE_SERVER: self.onRequestLeaveServer
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
                gameList[nickname] = { 'ip': self.ipAddress, 'port': p2pPort }
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
            availableGames = [{'nickname': key, 'ip': value['ip'], 'port': value['port']}
                            for key, value in gameList.items()
                            if key != requesterNickname] 
            response['id'] = ResponseMessageID.GET_AVAILABLE_GAMES_SUCCESS
            response['body'] = { 'availableGames': availableGames }

        response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
        self.connection.send(response)


    def onRequestJoinGame(self, requestParams):
        response = {}
        try:
            opponentName  = requestParams['nickname']
            opponentGuess = int(requestParams['guess'])
        except KeyError as error:
            response['id'] = ResponseMessageID.JOIN_GAME_ERROR
            response['body'] = { 'error': str(error) }
        else:
            startPlayer = 'server' if random.random() > opponentGuess else opponentName
            gameBoards[opponentName] = TicTacToe('server', opponentName, startPlayer)
            response['id'] = ResponseMessageID.JOIN_GAME_SUCCESS
            response['body'] = { 'startPlayer': startPlayer }

        response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
        self.connection.send(response)

    
    def onRequestMakeMove(self, requestParams):
        response = {}
        try:
            opponentName = requestParams['nickname']
            opponentMove = requestParams['move']
        except KeyError as error:
            response['id'] = ResponseMessageID.MAKE_MOVE_ERROR
            response['body'] = { 'error': str(error) }
        else:
            gameBoard = gameBoards[opponentName]
            if gameBoard.makeMove(opponentMove, opponentName):
                response['id'] = ResponseMessageID.MAKE_MOVE_SUCCESS
                response['body'] = None
            else:
                response['id'] = ResponseMessageID.MAKE_MOVE_ERROR
                response['body'] = { 'error': 'Invalid move' }

        response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
        self.connection.send(response)

    
    def onRequestGetMove(self, requestParams):
        response = {}
        try:
            opponentName = requestParams['nickname']
        except KeyError as error:
            response['id'] = ResponseMessageID.GET_MOVE_ERROR
            response['body'] = { 'error': str(error) }
        else:
            gameBoard = gameBoards[opponentName]
            move = (random.randint(0, 2), random.randint(0, 2))
            while not gameBoard.makeMove(move, 'server'):
                move = (random.randint(0, 2), random.randint(0, 2))

            response['id'] = ResponseMessageID.GET_MOVE_SUCCESS
            response['body'] = { 'nickname': 'server', 'move': move }
            response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
            self.connection.send(response)

        
    def onRequestEndGame(self, requestParams):
        opponentName = requestParams.get('nickname', None)
        gameBoards.pop(opponentName, None)
        response = { 'id': ResponseMessageID.END_GAME_ACK, 'body': None }
        response = json.dumps(response, cls=MessageEncoder).encode('utf-8')
        self.connection.send(response)


    def onRequestLeaveServer(self, requestParams):
        opponentName = requestParams.get('nickname', None)
        gameBoards.pop(opponentName, None)
        gameList.pop(opponentName, None)
        response = { 'id': ResponseMessageID.LEAVE_SERVER_ACK, 'body': None }
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
    requestHandlerThread = ClientThread(connection, address)
    print('created thread to handle request...')
    requestHandlerThread.start()
    print('handling request in separate thread')
