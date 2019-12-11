# Standard library imports
import socket
import json
import tkinter as tk
from tkinter import Tk, Label, Button
from functools import partial

# Third party library imports
from typing import Callable

# Local package imports
from client import Client
from message import RequestMessageID, ResponseMessageID, sendMSG

class GameGUI(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.mainFrame = tk.Frame(self)
        self.client = Client()
        self.pack()
        self.mainFrame.pack()
        self.createMainScreen()


    def createMainScreen(self):
        """ Creates the main screen when the GUI is launched allowing the user
        to connect to a game server with an IP Address and Port of their choice.
        """
        entryFrame = tk.Frame(self.mainFrame)
        serverIpLabel   = tk.Label(entryFrame, text='Server IP:')
        serverPortLabel = tk.Label(entryFrame, text='Server Port:')
        nicknameLabel   = tk.Label(entryFrame, text='Nickname:')
        p2pPortLabel    = tk.Label(entryFrame, text='P2P Port:')
        serverIpEntry   = tk.Entry(entryFrame)
        serverPortEntry = tk.Entry(entryFrame)
        nicknameEntry   = tk.Entry(entryFrame)
        p2pPortEntry    = tk.Entry(entryFrame)
        entryFrame.pack()
        serverIpLabel.grid(row=0, column=0)
        serverIpEntry.grid(row=0, column=1)
        serverPortLabel.grid(row=1, column=0)
        serverPortEntry.grid(row=1, column=1)
        nicknameLabel.grid(row=2, column=0)
        nicknameEntry.grid(row=2, column=1)
        p2pPortLabel.grid(row=3, column=0)
        p2pPortEntry.grid(row=3, column=1)

        buttonFrame   = tk.Frame(self.mainFrame)
        connectButton = tk.Button(buttonFrame, text='Connect')
        quitButton    = tk.Button(buttonFrame, text='QUIT', command=self.onQuit)
        buttonFrame.pack()
        connectButton.pack()
        quitButton.pack()

        errorMsgFrame = tk.Frame(self.mainFrame)
        errorMsgLabel = tk.Label(errorMsgFrame)
        errorMsgFrame.pack()
        errorMsgLabel.pack()

        def onConnectButtonPressed():
            def onSuccess():
                self.createGameRoomScreen()

            def onError(errorMsg=''):
                errorMsgLabel['text'] = errorMsg

            serverIP   = serverIpEntry.get()
            serverPort = serverPortEntry.get()
            nickname   = nicknameEntry.get()
            p2pPort    = p2pPortEntry.get()

            if serverIP and serverPort and nicknameEntry and p2pPort:
                self.connectToGameServer(serverIP, int(serverPort), onSuccess, onError)
                self.joinGameServer(nickname, int(p2pPort), onSuccess, onError)
            else:
                onError('All fields are required')

        connectButton['command'] = onConnectButtonPressed


    def createGameRoomScreen(self):
        """ Creates game room screen user sees once they have successfully
        connected to the game server. This screen will query the server for a
        list of available games and list them. The user will have the ability
        to join one of the available games or play agains the game server.
        """
        # Clear screen and deallocate all previous widgets
        if self.mainFrame is not None:
            self.mainFrame.destroy()
            self.mainFrame = tk.Frame(self)
            self.mainFrame.pack()

        menuBar         = tk.Frame(self.mainFrame)
        playComputerBtn = tk.Button(menuBar, text='Play computer')
        quitBtn         = tk.Button(menuBar, text='Quit', command=self.onQuit)
        menuBar.pack()
        playComputerBtn.grid(row=0, column=0)
        quitBtn.grid(row=0, column=1)

        errorMsgFrame = tk.Frame(self.mainFrame)
        errorMsgLabel = tk.Label(errorMsgFrame)
        errorMsgFrame.pack()
        errorMsgLabel.pack()

        try:
            availableGames = self.client.getListOfAvailableGames()
        except Exception as error:
            errorMsgLabel['text'] = str(error)
            return

        for game in availableGames:
            print(game)


    def connectToGameServer(self, ipAddr: str, port: int, onSuccess: Callable, onError: Callable[[str], None]):
        """ Connect to game server.

        Arguments:
        ----------
        ipAddr    - IP Address of game server
        port      - Port number that game server is listening on.
        onSuccess - Callback to be called if connection is successfull.
        onError   - Callback to be called if connection fails.
        """
        try:
            self.client.connectToServer(ipAddr, port)
        except Exception as error:
            onError(str(error))
        else:
            onSuccess()

    
    def joinGameServer(self, nickname: str, p2pPort: int, onSuccess: Callable, onError: Callable[[str], None]):
        try:
            self.client.joinServer(nickname, p2pPort)
        except Exception as error:
            # onError(str(error))
            pass
        else:
            onSuccess()


    def onQuit(self):
        """ Close all socket connections and close GUI. """
        self.client.closeServerConnection()
        self.client.closePeerConnection()
        self.master.destroy()

if __name__ == '__main__':
    root = Tk()
    root.minsize(256, 256)
    gui = GameGUI(root)
    root.mainloop()
