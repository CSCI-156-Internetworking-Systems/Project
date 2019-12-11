# Standard library imports
import socket
import json

# Third party library imports
from typing import List, Dict

# Local package imports
from message import (
    RequestMessageID, ResponseMessageID, MessageEncoder, MessageDecoder)

class Client():

    def __init__(self):
        self.serverSocket = None
        self.peerSocket = None
        self.nickname = None
        self.p2pPort = None 

    def connectToServer(self, ipAddr, port):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.connect((ipAddr, port))
        except Exception as error:
            print(str(error))
            self.serverSocket = None
            raise error 

    def connectToPeer(self, ipAddr, port):
        pass

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
            