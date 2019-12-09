import socket
import json
import tkinter as tk
from tkinter import Tk, Label, Button
from message_constants import RequestMessageID, ResponseMessageID, sendMSG

class TicTacToe:
    
    def __init__(self):
        self.__board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

class GameClient(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master          = master
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__peer_socket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pack()
        self.create_main_screen()

    def create_main_screen(self):
        self.connect_button = tk.Button(self, text='Connect to game server', command=self.connect_to_server)
        self.connect_button.pack()

        self.quit_button = tk.Button(self, text='QUIT', fg='red', command=self.master.destroy)
        self.quit_button.pack()

        self.info_label = tk.Label(self, text='')
        self.info_label.pack()

    def create_gameroom(self):
        # Clear screen and deallocate all previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()
        # Request game list from server
        game_list = self.get_game_list()
        print(game_list)
        
    def connect_to_server(self):
        try:
            self.__server_socket.connect(('0.0.0.0', 8080))
            self.info_label['text'] = 'Connected!'
            self.create_gameroom()
        except ConnectionRefusedError as error:
            self.info_label['text'] = 'Unable to connect {}'.format(str(error))

    def get_game_list(self):
        self.__server_socket.send(str.encode(json.dumps({
            'id': RequestMessageID.LIST_GAMES,
            'data': 'c'
        })))
        server_response = (self.__server_socket.recv(4096)).decode("utf-8")
        return server_response

if __name__ == '__main__':
    root = Tk()
    root.minsize(256, 256)
    gui = GameClient(root)
    root.mainloop()