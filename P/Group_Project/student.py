import asyncio
import getpass
import json
import os
import websockets
import time
from newBotFuncts import generateBoard, generateBoardWithGame, rotate, toStr
from tree_search import SearchNode, SearchTree

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # We start with a default value so that we can lock it later while the piece is falling
        newpiece = True 

        # Depth to search
        limit = 3

        # Current simulated board
        currentBoard = None

        # Prunning used during search
        prunning = 3

        # List of commands we are going to execute on the bot
        commands = []

        # Positions stored, this will helps us later on, if we have a new position array we add it, if not we can just grab it from this dict
        positionsDict = {}

        # Final score
        finalScore = 0

        # dimensions of the board
        dimensions = None

        # Reference the piece that we are analyzing
        counter_pieces = 0
        
        # The speed of the game in this moment
        gameSpeed = 0

        # Counter for response time
        totalTime  = 0
        times = 0
        
        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update, this must be called timely or your game will get out of sync with the server
                # Try to get a solution when we get a new piece
                if newpiece:
                    
                    newpiece = False    # We set it false so that we lock it and we dont try to get a solution every frame
                    
                    # Skip header info
                    if 'dimensions' in state:
                        dimensions = state['dimensions']
                        dimensions[0] -= 2
                        newpiece = True
                        continue

                    if 'game' in state:
                        game = state['game']    # Get current state of the board
                        # At the start of the game we simulate our board
                        if not currentBoard:
                            currentBoard = generateBoard(dimensions)
                        #toStr(currentBoard, dimensions)
                        #assert(currentBoard[:30] == generateBoardWithGame(game, dimensions))

                    if 'piece' in state:
                        piece = state['piece']  # Get current piece falling
                        counter_pieces += 1     

                        # Scuffed dsync scanner
                        if rotate(state['piece'])==[] and state['piece'] != None:
                            #print("DESYNC ON: " + str(state['piece']))
                            if counter_pieces == limit:
                                counter_pieces = 0
                            continue

                    if 'next_pieces' in state:
                        next_pieces = state['next_pieces']    # Get next pieces
                        
                    if 'score' in state:
                        finalScore = state['score']    # Get final score
                    
                    if 'game_speed' in state:
                        gameSpeed= state['game_speed']  #Gets the game speed

                    # DEBUG stuff
                    # print(state)
                    # print(piece)
                    # print(next_pieces)

                    # Skip the piece because we already have the commands
                    if counter_pieces <= limit and counter_pieces !=1:
                        piece = False

                    # Get all positions possible of a piece 
                    if piece: 
                        # Get an array with the current piece and the next pieces
                        total_pieces = [piece]
                        for p in next_pieces:
                            total_pieces += [p]
                        
                        
                        t = SearchTree(total_pieces, dimensions, currentBoard, limit, prunning)
                        tic = time.time() 
                        # print("chamei o search")
                        currentBoard, commands = t.search(positionsDict)
                        toc = time.time()
                        totalTime += toc - tic
                        times += 1

                        # toStr(currentBoard, dimensions)

                        if commands and commands != []:
                            comms = commands[counter_pieces -1]
                    else:
                        if commands and commands != []: 
                            comms = commands[counter_pieces -1]

                    # To stop advancing pieces because we will analyze a new piece
                    if counter_pieces == limit:
                        counter_pieces = 0
                        if gameSpeed==28:
                            limit=2
                        elif gameSpeed==50:
                            limit=1
                # If we have commands to send we send each cycle one
                elif comms != []:
                    await websocket.send(json.dumps({"cmd": "key", "key": comms[0]}))  # send key command to server 
                    comms = comms[1:]
                    # print(comms)

                # New piece comming so we need to try to predict our next move
                if 'piece' in state and state['piece'] == None and comms == []:
                    
                    newpiece = True

            except websockets.exceptions.ConnectionClosedOK:
                print("Final Score: ",finalScore)
                print("Response Time: ", totalTime/times)
                #print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
