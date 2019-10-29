import socket
import json
from message_constants import *

SERVER_IP = '0.0.0.0' # IP address where the server .py is being run, assumes port 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(client)
client.connect((SERVER_IP, 8080))
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
        if serverMsg['id'] == RES_GAME_CREATED:
            print("Game created, waiting for player to join.")
        else:
            print("Error, game not created.")
    elif userInput == 'j':
        sendMSG(client, REQ_GAME_LIST, "")

client.close()