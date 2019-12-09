import socket
import json
from message import RequestMessageID, ResponseMessageID, Message, sendMSG

# definitions of functions for switch dictionary:
def Exec_Game_List(mesgData):
    conn.send(json.dumps(gamesList).encode('utf-8'))

def Exec_Create_Game(msgData): # msgData in this case will be the name of the game/player being created
    gamesList.append((msgData, addr))
    print("Games: ", gamesList)
    sendMSG(conn, ResponseMessageID.GAME_CREATED, "") # no data, this is essentially just an ACK response

def Exec_Join_Game(msgData):
    pass

# dictionary of functions that get selected by the message IDs:
msgSwitchDict = {
    RequestMessageID.LIST_GAMES: Exec_Game_List,
    RequestMessageID.CREATE_GAME: Exec_Create_Game,
    RequestMessageID.JOIN_GAME:   Exec_Join_Game
}

# list of all connected players waiting for a second player to join them:
gamesList = []

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
while True:
    print("Waiting for message...")
    conn, addr = serv.accept()
    print("Message received.")
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client = json.loads(data.decode("utf-8"))
        print(from_client)
        msgSwitchDict[from_client['id']](from_client['data'])
        print("---Client Message---")
        print(from_client)
        print("--------------------")
    conn.close()
    print('client disconnected')
