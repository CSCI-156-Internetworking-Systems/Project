from os import system
class TicTacToe:
    
	def __init__(self, myNewName, newOpponentsName, startingTurnPlayer):
		self.__board = [
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]
		self.__myName = myNewName
		self.__opName = newOpponentsName
		self.__turnPlayer = startingTurnPlayer
#	def __str__(self):
#		ret = ""
#		for row in self.__board:
#			ret += str(row[0]) + str(row[1]) + str(row[2])
#		return ret[:-1]
#	def print(self):
#		ret = ""
#		for row in self.__board:
#			ret += "X" if row[0] == 1 else ("O" if row[0] == 2 else "-")
#			ret += "X" if row[1] == 1 else ("O" if row[1] == 2 else "-")
#			ret += "X" if row[2] == 1 else ("O" if row[2] == 2 else "-")
#			ret += "\n"
#		ret = ret[:-1]
#		print(ret)
	def getBoard(self):
		return self.__board
	def makeMove(self, position, attemptedTurnPlayer):
		if (self.__turnPlayer != attemptedTurnPlayer):
			return False
#		index = (3 * position[0]) + position[1]
		if (position[0] < 0) | (position[0] > 2) | (position[1] < 0) | (position[1] > 2):
			return False
#		if self.__board[int(index / 3)][index % 3] == 0:
#			self.__board[int(index / 3)][index % 3] = self.__turnPlayer
		if self.__board[position[0]][position[1]] == 0:
			self.__board[position[0]][position[1]] = self.__turnPlayer
			self.__turnPlayer = self.__myName if self.__turnPlayer == self.__opName else self.__opName
			return True
		return False
	def getTurnPlayer(self):
		return self.__turnPlayer
	def checkWinCondition(self):
		for row in self.__board:
			if ((row[0] == row[1]) & (row[1] == row[2]) & (row[0] != 0)):
				return row[0]

		if ((self.__board[0][0] == self.__board[1][0]) & (self.__board[1][0] == self.__board[2][0]) & (self.__board[0][0] != 0)):
			return self.__board[0][0]
		if ((self.__board[0][1] == self.__board[1][1]) & (self.__board[1][1] == self.__board[2][1]) & (self.__board[0][1] != 0)):
			return self.__board[0][1]
		if ((self.__board[0][2] == self.__board[1][2]) & (self.__board[1][2] == self.__board[2][2]) & (self.__board[0][2] != 0)):
			return self.__board[0][2]

		if ((self.__board[0][0] == self.__board[1][1]) & (self.__board[1][1] == self.__board[2][2]) & (self.__board[0][0] != 0)):
			return self.__board[0][0]
		if ((self.__board[0][2] == self.__board[1][1]) & (self.__board[1][1] == self.__board[2][0]) & (self.__board[0][2] != 0)):
			return self.__board[0][2]
		return 0


#board = TicTacToe(1, 2, 1)
#board.makeMove((3,-4),1)
#print(board.getBoard())
#board = TicTacToe(1)
##board.makeMove(0,"X")
#system('clear')
##print(board)
##board.print()
#print(board.getBoard())
#while 1:
#	index = int(input())
#	print("The move was:", "Successful" if board.makeMove(index) else "Unsuccessful")
#	system('clear')
##	print(board)
##	board.print()
#	print(board.getBoard())
#	print("Turn Player is: ", board.getTurnPlayer())
#	currentWinner = board.checkWinCondition()
#	print("The winner is: ", 'X' if currentWinner == 1 else 'O' if currentWinner == 2 else "No one")
