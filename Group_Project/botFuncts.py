import copy
#  board state info format
#
#       |        | ...       
#       |        | 27
#       |        | 28          
#       |        | 29
#       ---------- (29x29)
#        12345678

# Our board state info format
#
#       1 1 1 1 1 1 1 1   ==== in decimal ====> 255
# 
#  each "layer" (vertical position on the game) is represented with the int 256 (at start) we will change it later on to represent placed cubes there
# 
# ex:
#   bloco na posição x = 3
#   
#       1 0 1 1 1 1 1 1   ==== in decimal ====> 191
#       ^ ^ ^ ^ ^ ^ ^ ^
#       | | | | | | | |             
#       | | | | | | | '--> 8 position
#       | | | | | | '----> 7 position
#       | | | | | '------> 6 position 
#       | | | | '--------> 5 position
#       | | | '----------> 4 position
#       | | '------------> 3 position
#       | '--------------> 2 position
#       '----------------> 1 position

# X position calculation when dropping a block is relative to its positionning
#
#       <----|----|----|----|---|----|----|----|----> 
#     ... -4 | -3 | -2 | -1 | 0 | +1 | +2 | +3 | +4 ...


def boardSimulate(game, shapeToDrop=None, boardIsGiven=False):
    '''Create simulated board with the current game info and with the piece on the '''
    # Hard coded is the best coded 
    if boardIsGiven:
        board = list.copy(game)
    else:
        board = [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255]
        
        # Set board cubes
        for cube in game:
            board[cube[1]] = setBit(board[cube[1]], cube[0])
    
    dropped = False

    # If we want to try to drop the figure on the x position
    if shapeToDrop:    
        board, dropped = dropShape(board, shapeToDrop) 

    return (board, dropped)

def setBit(layer, position):
    '''Sets bit 0 on the int (bit represents the cube and the in represents the layer on the game)'''
    return layer ^ ((1<<(8 - position)))

def isSet(layer,position):
    '''Returns a bool of the value if the bit (cube) is 0 (is placed there) already or not'''
    return False if (layer & (1<<(8 - position))) != 0 else True 

def toStr(board):
    '''Just to print the board on output'''
    out = '\nNew board\n'
    for i in range(0,30):
        layer = "0"*(8-len(str(bin(board[i]))[2:])) + str(bin(board[i]))[2:] + '\n' 
        out += layer
    print(out, flush=True)

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

def translate(originalCords):
    '''Simulate translations of a piece, return tuple with possible translations'''
    possibletranslations = [(originalCords, [])]

    limit = False # used to check if we hitted a limit or not
    # Try translate to left until we hit a border
    for shift in range(-1,-8,-1):
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
    for shift in range(1,8):
        shiftedCords = []
        for cube in originalCords:
            shiftedCube = [0,0]
            shiftedCube[0] = cube[0] + shift
            shiftedCube[1] = cube[1] + shift

            # If cord are out of bounds we cant try to place it
            if 8 < shiftedCube[0]:
                limit = True
                break
            else:
                shiftedCords.append(shiftedCube)

        # If we hit a limit we dont need to try more to the right   
        if limit:
            break
        
        possibletranslations.append((shiftedCords, ["d" for i in range(shift)]))

    return possibletranslations

def positions(spawnPiece):
    '''Get all positions possible and commands to there of a given piece by giving their spawn position'''
    positions = []
    rotation_state = 0                          # used to know in wich rotation state we are in
    for rotation in rotate(spawnPiece):
        for position in translate(rotation):
            positions.append((position[0], ["w" for i in range(rotation_state)] + position[1]))
        rotation_state += 1 
    return positions 

def dropShape(board, shape):
    '''Check if we can drop a shape on a certain position and if so drop it there and return the simulated board with it dropped'''
    
    # Get maxY cube in piece
    maxY = 0
    for cube in shape:
        if cube[1] > maxY:
            maxY = cube[1]
    
    # Check if we dont hit a piece while spawning it
    for cube in shape:
        if isSet(board[cube[1]] , cube[0]):
            return (board, False)

    # Check if we hit some piece while dropping the shape
    for dropped in range(1,29 - maxY):
        # If the lowest row isnt clean
        if board[maxY + dropped] != 255:
            # Check if we can set the shape there
            for cube in shape:
                x = cube[0] 
                y = cube[1] + dropped

                # If we cant put it there that means we hitted a piece
                if isSet(board[y] , x):
                    # We can put the dropping piece on the previous position
                    for cube in shape:
                        x = cube[0]
                        y = cube[1] +  dropped - 1
                        board[y] = setBit(board[y] , x)
                    return (board, True)
            
    # If we hit the bottom of the board
    for cube in shape:
        x = cube[0]
        y = cube[1] +  dropped
        board[y] = setBit(board[y] , x)
    return (board, True)


def calcHoles(board):
    '''Calculate points in factor of holes presented on the simulated board'''
    underMask = 0
    lneighborMask = 0
    rneighborMask = 0
    foundHoles = 0
    minY = 3
    ysize = 30
    
    # Check where the blocks start apperaring on the board from the top to bottom
    for y in range(minY,ysize):
        # Check if row is empty, if not break loop
        if board[y] != 255:
            minY = y 
            break

    # Count holes 
    for y in range(minY,ysize):
        line = board[y] 
        filled = ~line & 255

        underMask |= filled
        lneighborMask |= (filled << 1)
        rneighborMask |= (filled >> 1)
        
        foundHoles += score(3, y)*setOnes(underMask & line)
        foundHoles += score(2, y)*setOnes(lneighborMask & line)
        foundHoles += score(2, y)*setOnes(rneighborMask & line)

    return foundHoles

def score(p,y):
    '''Give each hole its weight in function to its hight appearence'''
    result = 1
    for i in range(p):
        result = result * (30 - y)
    return result

def setOnes(num, position=1):
    # Terminal case
    if position == 9:
        return 0

    # If we have a bit set we add it to our counter and skip to the next position otherwise we just skip to the next position
    if not isSet(num,position):
        return setOnes(num, position + 1) + 1
    else:
        return setOnes(num, position + 1)