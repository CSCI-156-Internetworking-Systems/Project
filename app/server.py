import socket
import json
from message import (
    RequestMessageID, ResponseMessageID, Message, MessageEncoder, MessageDecoder, sendMSG)

# list of all connected players waiting for a second player to join them:
gameList = {} 

# definitions of functions for switch dictionary:
def Exec_Create_Game(msgData): # msgData in this case will be the name of the game/player being created
    # gameList.append((msgData, addr))
    # print("Games: ", gameList)
    # sendMSG(conn, ResponseMessageID.GAME_CREATED, "") # no data, this is essentially just an ACK response
    pass

def Exec_Join_Game(msgData):
    pass

def onRequestJoinServer(requestParams):
    response = {}
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
    conn.send(response)


def onRequestAvailbaleGames(requestParams):
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
    conn.send(response)

# dictionary of functions that get selected by the message IDs:
msgSwitchDict = {
    RequestMessageID.GET_AVAILABLE_GAMES: onRequestAvailbaleGames,
    RequestMessageID.CREATE_GAME: Exec_Create_Game,
    RequestMessageID.JOIN_GAME:   Exec_Join_Game,
    RequestMessageID.JOIN_SERVER: onRequestJoinServer
}

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 8080))
serv.listen()
serv.setblocking(False)
while True:
    print("Waiting for message...")
    conn, addr = serv.accept()
    print("Message received.")
    while True:
        data = conn.recv(4096)
        if not data:
            break
        request = json.loads(data.decode("utf-8"), cls=MessageDecoder)
        msgSwitchDict[request['id']](request['body'])
        print("---Client Message---")
        print(request)
        print("--------------------")
    conn.close()
    print('client disconnected')
