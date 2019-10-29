import socket
import json
from message_constants import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(client)
#client.connect(('192.168.1.72', 8080))
client.connect(('10.62.79.178', 8080)) # when at Fresno State
print("Connected to game server.")
while True:
    print("What would you like to do?")
    print("c - Create game\nj - Join Game")
    userInput = input()
    if userInput == 'c':
        print("Enter the name of your game to be shown to others:")
        userInput = input()

        sendMSG(client, REQ_CREATE_GAME, userInput)
        from_server = (client.recv(4096)).decode("utf-8")
        print("reseiving ", from_server)
        serverMsg = json.loads(from_server)
        if serverMsg['msgId'] == RES_GAME_CREATED:
            print("Game created, waiting for player to join.")
        else:
            print("Error, game not created.")
    elif userInput == 'j':
        client.send(str.encode('{"msgId" = %d, "data" = ""}' % (REQ_GAME_LIST)))

client.close()