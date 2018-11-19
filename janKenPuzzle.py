
#it will store all the solutions to all the possible boards
solutions = {}

#get the input and return the variables (int, int, list)
def readInput():

	line = list(map(int, input().rstrip().split()))

	rows = line[0]
	cols = line[1]

	board = []

	for i in range(rows):
		board.append(list(map(int, input().rstrip().split())))

	return rows, cols, board

#return true if a beats b
def beat(a, b):
	return b and ((b-a)%3==1)

#return a list of all the possible movements from (i, j)
def findLegalMovements(i, j, board, rows, cols):
	typeOfPiece = board[i][j]
	listOfMovements = []
	#up
	if i > 0 and beat(typeOfPiece, board[i-1][j]):
		listOfMovements.append([i-1, j])
	#left
	if j > 0 and beat(typeOfPiece, board[i][j-1]):
		listOfMovements.append([i, j-1])
	#down
	if i < rows-1 and beat(typeOfPiece, board[i+1][j]):
		listOfMovements.append([i+1, j])
	#right
	if j < cols-1 and beat(typeOfPiece, board[i][j+1]):
		listOfMovements.append([i, j+1])
	return listOfMovements


#store the solutions and return a tupled version of board
def findSolutions(board, rows, cols):
	boardTuple = tuple(tuple(row) for row in board)

	#check if the solution is not already calculated
	if(boardTuple not in solutions):
		numberOfPieces = 0
		firstPieceI = 0
		firstPieceJ = 0
		#loop through the board
		for i in range(rows):
			for j in range(cols):
				#if there is a piece
				if board[i][j] != 0:
					#increment the number of pieces
					numberOfPieces += 1
					if numberOfPieces == 1:
						#get the piece's position
						firstPieceI = i
						firstPieceJ = j
					#stop if numberOfPieces reach 2
					elif numberOfPieces == 2:
						break


		#add the board and its solution to solutions
		if(numberOfPieces == 1):
			solutions[boardTuple] = {(firstPieceI, firstPieceJ, boardTuple[firstPieceI][firstPieceJ]) : 1}

		else:
			solutions[boardTuple] = {}
			#for each position of the board
			for i in range(firstPieceI, rows):
				for j in range(0, cols):
					#if there is a piece
					if board[i][j] != 0:
						listOfMovements = findLegalMovements(i, j, board, rows, cols)
						for movement in listOfMovements:
							#move the piece
							capturedPiece = board[movement[0]][movement[1]]
							board[movement[0]][movement[1]] = board[i][j]
							board[i][j] = 0

							#find the solutions to the new board
							newBoard = findSolutions(board, rows, cols)

							#print(boardTuple)
							#take the current solutions
							currentSolutions = solutions[boardTuple]
							#take the new solutions
							newSolutions = solutions[newBoard]

							for finalState in newSolutions:
								currentSolutions[finalState] = currentSolutions.get(finalState, 0) + newSolutions[finalState]

							#move the piece back
							board[i][j] = board[movement[0]][movement[1]]
							board[movement[0]][movement[1]] = capturedPiece
	return boardTuple





#get the input, call the solver and print the output
def main():
	#get the input
	rows, cols, board = readInput()

	#find the solutions
	boardTuple = findSolutions(board, rows, cols)

	#print how many different solutions are there
	finalStates = solutions[boardTuple]
	nSolutions = 0
	for finalState in finalStates:
		nSolutions += finalStates[finalState]
	print(nSolutions)
	#print the number of final states
	print(len(finalStates), end='')
	#print the final states
	finalStates = list(finalStates.keys())
	finalStates.sort()
	for finalState in finalStates:
		print('\n' + str(finalState[0]+1) + ' ' + str(finalState[1]+1) + ' ' + str(finalState[2]), end='')


#allow this module to be imported
if __name__ == "__main__":
	main()
