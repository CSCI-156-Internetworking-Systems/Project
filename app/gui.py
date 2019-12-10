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
        self.client = Client()
        self.pack()
        self.createMainScreen()


    def createMainScreen(self):
        """ Creates the main screen when the GUI is launched allowing the user
        to connect to a game server with an IP Address and Port of their choice.
        """
        entryFrame = tk.Frame(self)
        ipLabel    = tk.Label(entryFrame, text='IP:')
        portLabel  = tk.Label(entryFrame, text='Port:')
        ipEntry    = tk.Entry(entryFrame)
        portEntry  = tk.Entry(entryFrame)
        entryFrame.pack()
        ipLabel.grid(row=0, column=0)
        ipEntry.grid(row=0, column=1)
        portLabel.grid(row=1, column=0)
        portEntry.grid(row=1, column=1)

        buttonFrame   = tk.Frame(self)
        connectButton = tk.Button(buttonFrame, text='Connect')
        quitButton    = tk.Button(buttonFrame, text='QUIT', command=self.onQuit)
        buttonFrame.pack()
        connectButton.pack()
        quitButton.pack()

        errorMsgFrame = tk.Frame(self)
        errorMsgLabel = tk.Label(errorMsgFrame)
        errorMsgFrame.pack()
        errorMsgLabel.pack()

        def onConnectButtonPressed():
            def onSuccess():
                self.createGameRoomScreen()

            def onError(errorMsg=''):
                errorMsgLabel['text'] = errorMsg

            if ipEntry.get() and portEntry.get():
                self.connectToGameServer(ipEntry.get(),
                                         int(portEntry.get()),
                                         onSuccess,
                                         onError)
            else:
                onError('IP Address or Port number missing')

        connectButton['command'] = onConnectButtonPressed;


    def createGameRoomScreen(self):
        """ Creates game room screen user sees once they have successfully
        connected to the game server. This screen will query the server for a
        list of available games and list them. The user will have the ability
        to join one of the available games or play agains the game server.
        """
        # Clear screen and deallocate all previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()


    def connectToGameServer(self, ipAddr: str, port: int, onSuccess: Callable, onError: Callable[str]) -> None:
        """
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
