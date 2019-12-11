# Standard library imports
import socket
import json
import random
import threading
import tkinter as tk
from tkinter import Tk, Label, Button
from functools import partial

# Third party library imports
from typing import Callable, List

# Local package imports
from client import Client
from message import RequestMessageID, ResponseMessageID, sendMSG
from game_logic import TicTacToe

class GameGUI(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.mainFrame = tk.Frame(self)
        self.client = Client()
        self.btnGrid = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]
        self.pack()
        self.mainFrame.pack()
        self.createMainScreen()


    def createMainScreen(self):
        """ Creates the main screen when the GUI is launched allowing the user
        to connect to a game server with an IP Address and Port of their choice.
        """
        userInputFrame  = tk.Frame(self.mainFrame)
        serverIpLabel   = tk.Label(userInputFrame, text='Server IP:')
        serverIpEntry   = tk.Entry(userInputFrame)
        serverPortLabel = tk.Label(userInputFrame, text='Server Port:')
        serverPortEntry = tk.Entry(userInputFrame)
        nicknameLabel   = tk.Label(userInputFrame, text='Nickname:')
        nicknameEntry   = tk.Entry(userInputFrame)
        p2pPortLabel    = tk.Label(userInputFrame, text='P2P Port:')
        p2pPortEntry    = tk.Entry(userInputFrame)
        userInputFrame.pack()
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
                serverPort = int(serverPort)
                p2pPort    = int(p2pPort)
                self.connectToGameServer(serverIP, serverPort, nickname, p2pPort, onSuccess, onError)
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

        welcomeBanner    = tk.Frame(self.mainFrame)
        welcomeBannerMsg = tk.Label(welcomeBanner, text='Welcome {}'.format(self.client.nickname))
        welcomeBanner.pack()
        welcomeBannerMsg.pack()

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

        def onPlayServerBtnPressed():
            def onError(errorMsg):
                errorMsgLabel['text'] = errorMsg
            self.playAgainstServer(onError)

        playComputerBtn['command'] = onPlayServerBtnPressed    

        self.availableGamesFrame = tk.Frame(self.mainFrame)
        availableGamesLable = tk.Label(self.availableGamesFrame, text='Available Games:')
        self.availableGamesFrame.pack()
        availableGamesLable.grid(row=0, column=0)

        self.updateListOfAvailableGames()


    def connectToGameServer(self, ipAddr: str, port: int, nickname: str, p2pPort: int, onSuccess: Callable, onError: Callable[[str], None]):
        """ Connect to game server.

        Arguments:
        ----------
        ipAddr    - IP Address of game server
        port      - Port number that game server is listening on.
        nickname  - Unique name of user on the game server
        p2pPort   - The port that the user will uses for P2P connection.
        onSuccess - Callback to be called if connection is successfull.
        onError   - Callback to be called if connection fails.
        """
        try:
            self.client.connectToServer(ipAddr, port)
            self.client.joinServer(nickname, p2pPort)
        except Exception as error:
            onError(str(error))
        else:
            onSuccess()

    
    def getListOfAvailableGames(self, onSuccess: Callable[[List], None], onError: Callable[[str], None]):
        try:
            availableGames = self.client.getListOfAvailableGames()
        except Exception as error:
            onError(str(error))
        else:
            onSuccess(availableGames)
    

    def updateListOfAvailableGames(self):
        def onSuccess(availableGames):
            if self.availableGamesFrame:
                self.availableGamesFrame.destroy()
                self.availableGamesFrame = tk.Frame(self.mainFrame)
                availableGamesLable = tk.Label(self.availableGamesFrame, text='Available Games:')
                self.availableGamesFrame.pack()
                availableGamesLable.grid(row=0, column=0)

            for game in availableGames:
                opponentName = tk.Label(self.availableGamesFrame, text=game['nickname'])
                joinGameBtn  = tk.Button(self.availableGamesFrame, text='Join') 
                opponentName.grid(row=1, column=0)
                joinGameBtn.grid(row=1, column=1)

        def onError(errorMsg):
            error = tk.Label(self.mainFrame, text=errorMsg)
            error.pack()

        self.getListOfAvailableGames(onSuccess, onError)
        self.updateJob = self.after(5000, self.updateListOfAvailableGames)

    
    def playAgainstServer(self, onError):
        if self.updateJob is not None:
            self.after_cancel(self.updateJob)
        try:
            self.client.joinGame('server')
        except Exception as error:
            onError(str(error))
        else:
            self.opponent = 'server'
            self.createTicTacToeScreen()
            if self.client.ticTacToe.getTurnPlayer() == 'server':
                self.getServerMove()


    def createTicTacToeScreen(self):
       # Clear screen and deallocate all previous widgets
        if self.mainFrame is not None:
            self.mainFrame.destroy()
            self.mainFrame = tk.Frame(self)
            self.mainFrame.pack() 

        buttonFrame  = tk.Frame(self.mainFrame)
        returnBtn    = tk.Button(buttonFrame,
                                 text='Return to Game Room',
                                 command=self.createGameRoomScreen)
        quitButton   = tk.Button(buttonFrame, text='QUIT', command=self.onQuit)
        buttonFrame.pack()
        returnBtn.pack()
        quitButton.pack()

        ticTacToeFrame = tk.Frame(self.mainFrame)
        ticTacToeFrame.pack()

        infoLabel = tk.Label(self.mainFrame)
        infoLabel['text'] = self.client.ticTacToe.getTurnPlayer() + "'s turn"
        infoLabel.pack()
 
        def onPositionPressed(row, col):
            def onSuccess():
                currentPlayer = self.client.ticTacToe.getTurnPlayer()
                infoLabel['text']  = currentPlayer + "'s turn"
                self.btnGrid[row][col]['text']  = 'X'

            def onError(errorMsg):
                infoLabel['text'] = errorMsg 

            self.makeMove(self.opponent, (row, col), onSuccess, onError)

            if self.client.ticTacToe.checkWinCondition():
                self.onHasWinner(self.client.ticTacToe.checkWinCondition(), infoLabel)
            elif not self.client.ticTacToe.hasPossibleMoves():
                self.onStaleMate(infoLabel)
            else:
                self.getServerMove()
                infoLabel['text'] = self.client.ticTacToe.getTurnPlayer() + "'s turn" 
                if self.client.ticTacToe.checkWinCondition():
                    self.onHasWinner(self.client.ticTacToe.checkWinCondition(), infoLabel)
                elif not self.client.ticTacToe.hasPossibleMoves():
                    self.onStaleMate(infoLabel)

        for row in range(0, 3):
            for col in range(0, 3):
                btn = tk.Button(ticTacToeFrame,
                                font='Times 20 bold',
                                bg='white',
                                fg='black',
                                height=2,
                                width=4)
                btn['command'] = partial(onPositionPressed, row, col)
                btn.grid(row=row, column=col)
                self.btnGrid[row][col] = btn

        
    def makeMove(self, opponent, move, onSuccess, onError):
        try:
            self.client.makeMove(self.opponent, move)
        except Exception as error:
            onError(str(error))
        else:
            onSuccess()


    def getServerMove(self):
        row, col = self.client.getMove('server')
        self.btnGrid[row][col]['text'] = 'O'
    

    def onHasWinner(self, winner, label):
        label['text'] = winner + ' Wins!!!'
        for row in self.btnGrid:
            for btn in row:
                btn['state'] = 'disabled'

    
    def onStaleMate(self, label):
        label['text'] = 'Stale Mate!'
        for row in self.btnGrid:
            for btn in row:
                btn['state'] = 'disabled'


    def onQuit(self):
        """ Close all socket connections and close GUI. """
        self.client.leaveServer()
        self.master.destroy()


if __name__ == '__main__':
    root = Tk()
    root.minsize(256, 256)
    gui = GameGUI(root)
    root.mainloop()
