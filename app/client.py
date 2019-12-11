# Standard library imports
import socket
import json
import random

# Third party library imports
from typing import List, Dict

# Local package imports
from message import (
    RequestMessageID, ResponseMessageID, MessageEncoder, MessageDecoder)

from game_logic import TicTacToe

class Client():

    def __init__(self):
        self.serverSocket = None
        self.peerSocket = None
        self.nickname = None
        self.p2pPort = None
        self.ticTacToe = None


    def connectToServer(self, ipAddr, port):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.connect((ipAddr, port))
        except Exception as error:
            print(str(error))
            self.serverSocket = None
            raise error 


    def connectToPeer(self, ipAddr, port):
        try:
            self.peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peerSocket.connect((ipAddr, port))
        except Exception as error:
            print(str(error))
            self.serverSocket = None
            raise error 


    def closeServerConnection(self):
        if self.serverSocket is not None:
            self.serverSocket.close()


    def closePeerConnection(self):
        if self.peerSocket is not None:
            self.peerSocket.close()


    def joinServer(self, nickname: str, p2pPort: int) -> bool:
        if self.serverSocket:
            request = {
                'id': RequestMessageID.JOIN_SERVER,
                'body': {
                    'nickname': nickname,
                    'p2pPort': p2pPort
                }
            }

            request = json.dumps(request, cls=MessageEncoder).encode('utf-8')
            self.serverSocket.send(request)

            response = self.serverSocket.recv(4096)
            response = json.loads(response.decode('utf-8'), cls=MessageDecoder)

            if response['id'] == ResponseMessageID.JOIN_SERVER_SUCCESS:
                self.nickname = nickname
                self.p2pPort = p2pPort
            else:
                raise  Exception(response['body']['error'])
        else:
            raise Exception('Error: not connected to server')


    def getListOfAvailableGames(self) -> List[Dict]:
        if self.serverSocket:
            request = {
                'id': RequestMessageID.GET_AVAILABLE_GAMES,
                'body': { 'nickname': self.nickname }
            }
            self.serverSocket.send(
                json.dumps(request, cls=MessageEncoder).encode('utf-8'))

            response = self.serverSocket.recv(4096)
            response = json.loads(response.decode('utf-8'), cls=MessageDecoder)

            if response['id'] == ResponseMessageID.GET_AVAILABLE_GAMES_SUCCESS:
                return response['body']['availableGames']
            else:
                raise Exception(response['body']['error'])

    
    def joinGame(self, opponentName, peerIP=None, peerPort=None):
        request = { 'id': RequestMessageID.JOIN_GAME }
        request['body'] = {
            'nickname': self.nickname,
            'guess': random.random()
        }
        request = json.dumps(request, cls=MessageEncoder).encode('utf-8')

        if opponentName == 'server':
            self.serverSocket.send(request)
        else:
            try:
                self.connectToPeer(peerIP, peerPort)
            except:
                raise Exception('Error: unable to connect to peer')
            else:
                self.peerSocket.send(request)

        response = self.serverSocket.recv(4096)
        response = json.loads(response.decode('utf-8'), cls=MessageDecoder)

        if response['id'] == ResponseMessageID.JOIN_GAME_SUCCESS:
            startPlayer = response['body']['startPlayer']
            self.ticTacToe = TicTacToe(self.nickname, opponentName, startPlayer)
            return startPlayer
        else:
            raise Exception(response['body']['error'])


    def makeMove(self, opponentName, move):
        request = { 'id': RequestMessageID.MAKE_MOVE }
        request['body'] = { 'nickname': self.nickname, 'move': move }
        request = json.dumps(request, cls=MessageEncoder).encode('utf-8')

        if opponentName == 'server':
            self.serverSocket.send(request)
        else:
            self.peerSocket.send(request)

        response = self.serverSocket.recv(4096)
        response = json.loads(response.decode('utf-8'), cls=MessageDecoder) 

        if response['id'] == ResponseMessageID.MAKE_MOVE_SUCCESS:
            self.ticTacToe.makeMove(move, self.nickname)
        else:
            raise Exception(response['body']['error'])

    
    def getMove(self, opponentName):
        request = { 'id': RequestMessageID.GET_MOVE }
        request['body'] = { 'nickname': self.nickname }
        request = json.dumps(request, cls=MessageEncoder).encode('utf-8')

        if opponentName == 'server':
            self.serverSocket.send(request)
        else:
            self.peerSocket.send(request)

        response = self.serverSocket.recv(4096)
        response = json.loads(response.decode('utf-8'), cls=MessageDecoder)

        if response['id'] == ResponseMessageID.GET_MOVE_SUCCESS:
            move = response['body']['move'] 
            self.ticTacToe.makeMove(move, opponentName)
            return move
        else:
            raise Exception(response['body']['error'])


    def endGame(self, opponentName):
        request = { 'id': RequestMessageID.END_GAME }
        request['body'] = { 'nickname': self.nickname }
        request = json.dumps(request, cls=MessageEncoder).encode('utf-8')

        if opponentName == 'server':
            self.serverSocket.send(request)
        else:
            self.peerSocket.send(request)

        response = self.serverSocket.recv(4096)
        response = json.loads(response.decode('utf-8'), cls=MessageDecoder)

        if response['id'] == ResponseMessageID.END_GAME_ACK:
            self.closePeerConnection()
            self.ticTacToe = None


    def leaveServer(self):
        request = { 'id': RequestMessageID.LEAVE_SERVER }
        request['body'] = { 'nickname': self.nickname }
        request = json.dumps(request, cls=MessageEncoder).encode('utf-8')

        if self.peerSocket:
            self.peerSocket.send(request)
        self.serverSocket.send(request)

        # response = self.serverSocket.recv(4096)
        # response = json.loads(response.decode('utf-8'), cls=MessageDecoder)

        # if response['id'] == ResponseMessageID.END_GAME_ACK:
        self.ticTacToe = None
        self.closePeerConnection()
        self.closeServerConnection()