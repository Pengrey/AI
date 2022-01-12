from newBotFuncts import dropShape, positions, Score, rotate, toStr, Nmaxelements

class SearchNode:
    def __init__(self, state, position, command, dimensions, board, cost, parent = None): 
        self.state = state              # piece state (str(piece))
        self.position = position        # position of the action taken
        self.command = command          # commands to execute the action
        self.dimensions = dimensions    # dimensions of the board of the game
        self.board = board              # simulated board of the action taken
        self.cost = cost                # cost of the action taken
        self.parent = parent            # parent node
    def __str__(self):
        return "Piece(" + str(self.position) + str(self.command) + "," + str(self.cost) + ")"
    def __repr__(self):
        return str(self)


# Arvores de pesquisa
class SearchTree:
    def __init__(self, pieces, dimensions, board, limit, prunning = 1):
        self.pieces = pieces            # pieces to search with (array of pieces coords where the first is the currently working piece)
        self.board = board              # current simulated game state to search on
        self.dimensions = dimensions    # dimensions of the board of the game
        self.limit = limit              # how many pieces are we going to evaluate
        self.prunning = prunning        # limit of nodes we want to take to search on the deeper depths
        self.depth = 0                  # depth of we are currently on
        self.nodes = []                 # list of piece nodes we are going to work during the search

    # obter o caminho (sequencia de estados) da raiz ate um no
    def getCommands(self,node):
        if node.parent == None:
            return node.command
        return self.getCommands(node.parent) + [node.command + ['s']] 
        
    # procurar a solucao
    def search(self, positionsDict):
        rootNode = SearchNode(str(self.pieces[0]), self.pieces[0], [], self.dimensions, self.board, 0)   # Root node for guidance
        previousNodes = [rootNode]  # Nodes to be used to start searches
        
        # Fix the coordinates of the next_pieces
        for p in self.pieces[1:self.limit]:   
            #if rotate(str(p)) == []:
            for coord in p:
                coord[0]+=2
                coord[1]+=1

        while True: # Iteration over depth of the search 
            lnewnodes = []              # Nodes we discover during search

            # Check on positions cache
            if str(self.pieces[0]) in positionsDict:
                allPositions = positionsDict[str(self.pieces[0])]    # If in the dictionary, get that piece positions
            else:
                allPositions = positions(self.pieces[0], self.dimensions)  # If not, we compute it
                positionsDict[str(self.pieces[0])] = allPositions    # Then get we add it for later use
                
            # Create nodes for every position starting from every previous nodes:
            for pNode in previousNodes:
                for position in allPositions:
                    board, dropped = dropShape(pNode.board, self.dimensions, position[0])
                    
                    if dropped:
                        score, clearedLines = Score(board, self.dimensions)

                        # We cut the layers that are clearedLines
                        layer = sum([1<<posi for posi in range(self.dimensions[0])]) # empty layer on a board
                        for line in clearedLines:
                            board.pop(line)
                            board = [layer] + board

                        #toStr(board, self.dimensions)

                        # We create a new node
                        nNode = SearchNode(str(position[0]), position[0], position[1], self.dimensions, board, score + pNode.cost, pNode)
                        lnewnodes.append(nNode)

            
            # Get top prunning of lnewnodes and return it to use on the next deeper searches
            if len(lnewnodes) > self.prunning:
                lnewnodes = Nmaxelements(lnewnodes, self.prunning)
            else:
                lnewnodes.sort(key=lambda x: x.cost, reverse=True)

            # Old way
            # lnewnodes.sort(key=lambda x: x.cost, reverse=True)
            # lnewnodes = lnewnodes[:self.prunning]

            # We are done with this depth search, we try to go to the next depth
            self.pieces = self.pieces[1:]   # We take out the first pieceID to try to search the next pieceID
            self.depth += 1 # We going deeper
            
            # If we it the bottom of our search we try to get the best value and retrieve the board, commands and dictionary(?)
            if self.depth == self.limit:
                # Get best node from the search
                # print("lnewnodes:")
                # print(lnewnodes)
                if lnewnodes != []:
                    bestNode = lnewnodes[0]
                    # print("bestnode:")
                    # print(str(bestNode) + str(bestNode.command))

                    # Get best node's board
                    board = bestNode.board
                    # toStr(board, self.dimensions)
                    # Retrieve commands for the states
                    commands = self.getCommands(bestNode)
                    # print("commands: ")
                    # print(commands)
                    return (board, commands)
                else:
                    return (None, [])
            else: # If we didnt ended our search we prepare the info we got to be reused
                previousNodes = lnewnodes
