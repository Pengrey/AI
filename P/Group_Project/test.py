from newBotFuncts import *

# Test board dimensions generation
dimensions = [8, 30]
board = generateBoard(dimensions)

# Test drop shapes
shape1 = [[1, 3], [1, 4], [1, 5], [1, 6]]
shape2 = [[1, 2], [2, 2], [3, 2], [4, 2]]
shape3 = [[4, 5], [3, 6], [4, 6], [5, 6]]
shape4 = [[5, 2], [6, 2], [7, 2], [8, 2]]

#shape1 = [[1, 2], [2, 2], [3, 2], [4, 2]]
#shape2 = [[5, 2], [6, 2], [7, 2], [8, 2]]
#shape3 = [[1, 2], [2, 2], [3, 2], [4, 2]]
#shape4 = [[5, 2], [6, 2], [7, 2], [8, 2]]

print("Dropping shape1")
board, dropped = dropShape(board, dimensions, shape1)

print("Dropping shape2")
board, dropped = dropShape(board, dimensions, shape2)

print("Dropping shape3")
board, dropped = dropShape(board, dimensions, shape3)

print("Dropping shape4")
board, dropped = dropShape(board, dimensions, shape4)

toStr(board, dimensions)

print(Score(board, dimensions))