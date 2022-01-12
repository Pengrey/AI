def generateBoard(dimensions):
    '''Generates a bitwise simulation of a new board'''
    layer = sum([1<<posi for posi in range(dimensions[0])])
    return [layer for i in range(dimensions[1])] + [0]

def generateBoardWithGame(game, dimensions):
    '''Generates a bit wise simulation of a new board with given game info'''
    layer = sum([1<<posi for posi in range(dimensions[0])])
    board = [layer for i in range(dimensions[1])]

    # Sets game info onto board
    for cube in game:
            board[cube[1]] = setBit(board[cube[1]], cube[0], dimensions)
    return board

def setBit(layer, position, dimensions):
    '''Sets bit 0 on the int (bit represents the cube setted on the board and the int represents the layer on the game)'''
    return layer ^ ((1<<(dimensions[0] - position)))

def isSet(layer,position, dimensions):
    '''Returns a bool of the value if the bit (cube) is 0 (is placed there) already or not'''
    return False if (layer & (1<<(dimensions[0] - position))) != 0 else True 

def toStr(board, dimensions):
    '''Just to print the board on output'''
    out = '\nNew board\n'
    for i in range(dimensions[1]):
        layer =  "0"*(len(str(dimensions[1])) - len(str(i))) + str(i) + " " + "0"*(dimensions[0]-len(str(bin(board[i]))[2:])) + str(bin(board[i]))[2:] + '\n' 
        out += layer
    print(out, flush=True)
    print("Cubes used: ",board[dimensions[1]])

# TODO Change this to work with dynamic board
def rotate(originalCords):
    '''Simulate rotation of a piece, return tuple with possible rotations'''
    states = {'[[2, 2], [3, 2], [4, 2], [5, 2]]' : [[[2, 2], [3, 2], [4, 2], [5, 2]],[[4, 3], [4, 4], [4, 5], [4, 6]]], 
              '[[3, 3], [4, 3], [3, 4], [4, 4]]' : [[[3, 3], [4, 3], [3, 4], [4, 4]]], 
              '[[4, 2], [4, 3], [5, 3], [5, 4]]' : [[[4, 2], [4, 3], [5, 3], [5, 4]],[[4, 3], [5, 3], [3, 4], [4, 4]]],
              '[[4, 2], [3, 3], [4, 3], [3, 4]]' : [[[4, 2], [3, 3], [4, 3], [3, 4]],[[3, 3], [4, 3], [4, 4], [5, 4]]],
              '[[4, 2], [5, 2], [4, 3], [4, 4]]' : [[[4, 2], [5, 2], [4, 3], [4, 4]],[[3, 3], [4, 3], [5, 3], [5, 4]], [[4, 4], [4, 5], [3, 6], [4, 6]], [[3, 5], [3, 6], [4, 6], [5, 6]]],
              '[[4, 2], [4, 3], [4, 4], [5, 4]]' : [[[4, 2], [4, 3], [4, 4], [5, 4]],[[3, 3], [4, 3], [5, 3], [3, 4]], [[3, 4], [4, 4], [4, 5], [4, 6]], [[5, 6], [3, 7], [4, 7], [5, 7]]],
              '[[4, 2], [4, 3], [5, 3], [4, 4]]' : [[[4, 2], [4, 3], [5, 3], [4, 4]],[[3, 3], [4, 3], [5, 3], [4, 4]], [[4, 4], [3, 5], [4, 5], [4, 6]], [[4, 5], [3, 6], [4, 6], [5, 6]]]
              }
    key = str(originalCords)
    if key in states:
        return states[key]
    else: 
        return []

def translate(originalCords, dimensions):
    '''Simulate translations of a piece, return tuple with possible translations'''
    possibletranslations = [(originalCords, [])]

    limit = False # used to check if we hitted a limit or not
    # Try translate to left until we hit a border
    for shift in range(-1,-dimensions[0],-1):
        shiftedCords = []
        for cube in originalCords:
            shiftedCube = [0,0]
            shiftedCube[0] = cube[0] + shift
            shiftedCube[1] = cube[1] - shift

            # If cord are out of bounds we cant try to place it
            if shiftedCube[0] < 1:
                limit = True
                break
            else:
                shiftedCords.append(shiftedCube)
        
        # If we hit a limit we dont need to try more to the left
        if limit:
            break

        possibletranslations.append((shiftedCords, ["a" for i in range(-shift)]))
    
    limit = False # used to check if we hitted a limit or not
    # Try translate to right until we hit a border
    for shift in range(1,dimensions[0]):
        shiftedCords = []
        for cube in originalCords:
            shiftedCube = [0,0]
            shiftedCube[0] = cube[0] + shift
            shiftedCube[1] = cube[1] + shift

            # If cord are out of bounds we cant try to place it
            if dimensions[0] < shiftedCube[0]:
                limit = True
                break
            else:
                shiftedCords.append(shiftedCube)

        # If we hit a limit we dont need to try more to the right   
        if limit:
            break
        
        possibletranslations.append((shiftedCords, ["d" for i in range(shift)]))

    return possibletranslations

def positions(spawnPiece, dimensions):
    '''Get all positions possible and commands to there of a given piece by giving their spawn position'''
    positions = []
    rotation_state = 0                                                                      # used to know in wich rotation state we are in
    for rotation in rotate(spawnPiece):
        for position in translate(rotation, dimensions):
            positions.append((position[0], ["w" for i in range(rotation_state)] + position[1]))
        rotation_state += 1 
    return positions

def dropShape(originalBoard, dimensions, shape):
    '''Simulate a piece to be drop on '''
    # copy original board to work on
    board = list.copy(originalBoard)

    # Get maxY cube in piece
    maxY = 0
    for cube in shape:
        if cube[1] > maxY:
            maxY = cube[1]
    
    # Check if we dont hit a piece while spawning it TODO check full translation path
    for cube in shape:
        if isSet(board[cube[1]] , cube[0], dimensions):
            return (board, False)

    # Check if we hit some piece while dropping the shape
    for dropped in range(maxY,dimensions[1] - maxY):
        # If the lowest row isnt clean
        if board[maxY + dropped] != board[0]:
            # Check if we can set the shape there
            for cube in shape:
                x = cube[0] 
                y = cube[1] + dropped
                # If we cant put it there that means we hitted a piece
                if isSet(board[y] , x, dimensions):
                    # We can put the dropping piece on the previous position
                    for i in range(len(shape)):
                        cube = shape[i]
                        x = cube[0]
                        y = cube[1] +  dropped - 1
                        # Backtrack if place is filled already (it happens when path is blocked)
                        if isSet(board[y] , x, dimensions):
                            for j in range(i):
                                cube = shape[j]
                                x = cube[0]
                                y = cube[1] +  dropped - 1
                                board[y] = setBit(board[y], x, dimensions)
                            return (board, False)

                        board[y] = setBit(board[y], x, dimensions)
                        
                        # Add one cube to the number of cubes in the board
                        board[dimensions[1]] += 1
                    return (board, True)
            
    # If we hit the bottom of the board
    for cube in shape:
        x = cube[0]
        y = cube[1] + dimensions[1] - maxY - 1
        board[y] = setBit(board[y], x, dimensions)
        # Add one cube to the number of cubes in the board
        board[dimensions[1]] += 1
    return (board, True)

# Heuristic taken from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
def Score(board, dimensions):
    '''Give total score for a given board and an array of the cleared lines'''
    score = 0                                                                               # final score for a given board
    heights = [0 for i in range(dimensions[0])]                                             # max height for each column
    clearedLines = []                                                                       # number of lines cleared
    bumpiness = 0                                                                           # bumpiness of a given board 

    # Heuristics taken
    a = -0.510066 # -0.510066 
    b =  0.760666 #  0.760666
    c = -0.356630 # -0.356630
    d = -0.184483 # -0.184483

    # Calculate Aggregate Height and Completed lines
    numClearedLines = 0
    heightsFound = 0                                                                        # number of heights found for columns
    for y in range(1,dimensions[1]):                                                        # Iterate over each layer of the board, with exception the first one
        if board[y] != board[0]:                                                            # If the layer isnt empty
            if heightsFound != dimensions[0]:                                               # Check if we still need to get column heights
                heightsFound += checkPlaced(board, y, dimensions, heights)                  # Get max heights present on that layer
        if board[y] == 0:                                                                   # we found a cleared line
            clearedLines += [y]                                                             # We increment the cleared lines number
            numClearedLines += 1
    
    # We calculate the agregated height at the end
    aggregateHeight = sum(heights) 

    # Calculate number of holes
    numberOfHoles = aggregateHeight - board[dimensions[1]]                                 # Original idea from Diogo Monteiro nmec: 97606, Lucius Vinicius nmec: 96123 and Afonso Campos nmerc: 100055
    
    # take out the cleared lines from the number of blocks on the board cuz they will be cleared
    board[dimensions[1]] -= numClearedLines*dimensions[0]

    aggregateHeight -= numClearedLines

    # Calculate bumpiness
    for col in range(dimensions[0] - 1):
        bumpiness += abs(heights[col] - heights[col + 1])

    score += a*aggregateHeight + b*numClearedLines + c*numberOfHoles + d*bumpiness
    return (score, clearedLines)

def checkPlaced(board, y, dimensions, heightsArray):
    '''Get max heights for each column and puts them on the array, returns number of max columns found in a given layer'''
    maxHeightsFound = 0
    # For each position on a layer
    for x in range(dimensions[0]):
        if isSet(board[y], x + 1, dimensions) and heightsArray[x] == 0:
            heightsArray[x] = dimensions[1] - y
            maxHeightsFound += 1
    return maxHeightsFound

# Function returns N largest elements
def Nmaxelements(list1, N):
    final_list = []
  
    for i in range(0, N): 
        max1 = None
          
        for j in range(len(list1)):     
            if max1 == None or list1[j].cost > max1.cost:
                max1 = list1[j];
                  
        list1.remove(max1);
        final_list.append(max1)
    return final_list