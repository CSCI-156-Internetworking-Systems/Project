#from os import system
class TicTacToe:
    
	def __init__(self):
		self.__board = [
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]
		self.__turnPlayer = 1
	def __str__(self):
		ret = ""
		for row in self.__board:
			ret += str(row[0]) + str(row[1]) + str(row[2])
		return ret[:-1]
	def print(self):
		ret = ""
		for row in self.__board:
			ret += "X" if row[0] == 1 else ("O" if row[0] == 2 else "-")
			ret += "X" if row[1] == 1 else ("O" if row[1] == 2 else "-")
			ret += "X" if row[2] == 1 else ("O" if row[2] == 2 else "-")
			ret += "\n"
		ret = ret[:-1]
		print(ret)
	def makeMove(self, index):
		if (index < 0) | (index > 8):
			return
		if self.__board[int(index / 3)][index % 3] == 0:
			self.__board[int(index / 3)][index % 3] = self.__turnPlayer
			self.__turnPlayer = 1 if self.__turnPlayer == 2 else 2
	def getTurnPlayer(self):
		return self.__turnPlayer
	def checkWinCondition(self):
		for row in self.__board:
			if ((row[0] == row[1]) & (row[1] == row[2]) & (row[0] != 0)):
				return row[0]
		if ((self.__board[0][0] == self.__board[1][1]) & (self.__board[1][1] == self.__board[2][2]) & (self.__board[0][0] != 0)):
			return self.__board[0][0]
		if ((self.__board[0][2] == self.__board[1][1]) & (self.__board[1][1] == self.__board[2][0]) & (self.__board[0][2] != 0)):
			return self.__board[0][2]
		return 0


#board = TicTacToe()
##board.makeMove(0,"X")
#system('clear')
##print(board)
#board.print()
#while 1:
#	index = int(input())
#	board.makeMove(index)
#	system('clear')
##	print(board)
#	board.print()
#	print("Turn Player is: ", board.getTurnPlayer())
#	currentWinner = board.checkWinCondition()
#	print("The winner is: ", 'X' if currentWinner == 1 else 'O' if currentWinner == 2 else "No one")
