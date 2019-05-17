import json
import re
import sys


#Function to perform the move on the board
#'player_computer' is used to store the moves played throughout the game 
#'state' contains the board indices and whether each spot is filled or empty
def play(move, player_computer, BoardState, state, flagPlayer):
    #First we check if this move is valid and return the state and a flag
	#if this flag is false it means the move is invalid and the play function returns '0' as in failed.
    state, flag = checkPlay(move, state)
    if flag == False:
        return player_computer, BoardState, state, 0
    if player_computer == '':
        player_computer = move
    else:
        #if the move is valid so it will be stored in 'player_computer' string
        player_computer = player_computer + ',' + move

    #'flagPlayer' is a flag that determines whose turn it is to play, i.e
  		#if it's the 1st player's turn then 'X' will be positioned in the 'move' position
  		#if it's the 2nd player's turn then 'O' will be positioned in the 'move' position
  		#'move' is the index of the player's spot of choice
  	#'BoardState' contains the Board's content
    if flagPlayer:
        BoardState = BoardState.replace(move + '*-', move + 'X')
    else:
        BoardState = BoardState.replace(move + '*-', move + 'O')
    return player_computer, BoardState, state, 1

#Function to check validity of the move
#state is json object consists of "col" 7 values, "row" which is the first empty row and "filled" which indicated whether the column 
#is filled or not
def checkPlay(move, state):
    row = int(move[0])
    col = int(move[1])
    #We only have 7 columns, if the move is not < 8 return false as it is invalid
    if not col < 8:
        return state, False
        #if this index is not filled yet
        #col-1 as the index of the array begins with 0
    if state[col - 1]['col'] == col and state[col - 1]['row'] == row and state[col - 1]['filled'] == False:
        #first mark it as filled
        state[col - 1]['filled'] == True
        #and if we still haven't reached the final row:
        if state[col - 1]['row'] != 6:
            #put the symbol in the upper row
            state[col - 1]['row'] = state[col - 1]['row'] + 1
        else:
            #else do nothing
            state[col - 1]['filled'] = True
        return state, True
    #if none of the above work, it probably means either the index was occupied (filled) or
    #any other possibility that makes the move invalid, so return False
    return state, False

#Function to print the Board with it's content according to the 2 strings of the computer and the player
def printBoard(BoardState):
    # ; is column separator
    board = BoardState.split(';')
    print("  1 2 3 4 5 6 7")
    for i in range(len(board)):
        print(len(board) - i, re.sub('[0-9]', '',board[len(board) - i - 1].replace(',', ' ').replace('*', '')))

def sortVertical(val): 
    return val[1] + val[0] 

#Function to check if anyone is in a winning state
def checkIfWin(computer, player):
    #stack the plays each one's made 
    player = player.split(",")
    computer = computer.split(",")
    
    #If the number of plays is less than 4, then no one is a winner of course, the function return 'None'
    if len(player) < 4 and len(computer) < 4:
        return "None"
    
    #sort it into the regular shape we know in order to make it easier to detect complete sequences 
    #first sort horizontally and the vertically
    horizontalPlayer = sorted(player)  
    player.sort(key = sortVertical)
    horizontalComputer = sorted(computer)
    computer.sort(key = sortVertical)
    
    #loop over each player's sorted stored moves
    for i in range(len(player)):
        try:
            #if 4 symbols are detected in the same row, check if their columns are successive, if true, return the winner
            if horizontalPlayer[i + 0][0] == horizontalPlayer[i + 1][0] == horizontalPlayer[i + 2][0] == horizontalPlayer[i + 3][0]:
                if (int(horizontalPlayer[i + 0][1]) - int(horizontalPlayer[i + 1][1]) == -1 and 
                    int(horizontalPlayer[i + 1][1]) - int(horizontalPlayer[i + 2][1]) == -1 and 
                    int(horizontalPlayer[i + 2][1]) - int(horizontalPlayer[i + 3][1]) == -1):
                    return "Player"
            
            #same as previous but for columns
            if player[i + 0][1] == player[i + 1][1] == player[i + 2][1] == player[i + 3][1]:
                if (int(player[i + 0][0]) - int(player[i + 1][0]) == -1 and 
                    int(player[i + 1][0]) - int(player[i + 2][0]) == -1 and 
                    int(player[i + 2][0]) - int(player[i + 3][0]) == -1):
                    return "Player"
        except:
            break
    
    #same as previous but for computer
    for i in range(len(computer)):
        try:
            if horizontalComputer[i + 0][0] == horizontalComputer[i + 1][0] == horizontalComputer[i + 2][0] == horizontalComputer[i + 3][0]:
                if (int(horizontalComputer[i + 0][1]) - int(horizontalComputer[i + 1][1]) == -1 and 
                    int(horizontalComputer[i + 1][1]) - int(horizontalComputer[i + 2][1]) == -1 and 
                    int(horizontalComputer[i + 2][1]) - int(horizontalComputer[i + 3][1]) == -1):
                    return "Computer"
            if computer[i + 0][1] == computer[i + 1][1] == computer[i + 2][1] == computer[i + 3][1]:
                if (int(computer[i + 0][0]) - int(computer[i + 1][0]) == -1 and 
                    int(computer[i + 1][0]) - int(computer[i + 2][0]) == -1 and 
                    int(computer[i + 2][0]) - int(computer[i + 3][0]) == -1):
                    return "Computer"
        except:
            break
    
    #initialize each diagonals starting point
    rDiagonal = ['11', '12', '13', '21', '22', '23', '31', '32', '33']
    lDiagonal = ['15', '16', '17', '25', '26', '27', '35', '36', '37']
    diagonal = ['14', '24', '34']

    #first for diagonals with positive slope,
    #check if any of the starting points exists in the player's moves
    #if yes, check if the rest of sequence also exists, if yes then you have a winner!
    for i in range(len(rDiagonal)):
        if rDiagonal[i] in player:
            num = str(int(rDiagonal[i][0]) + 1) + str(int(rDiagonal[i][1]) + 1)
            if num in player:
                num = str(int(rDiagonal[i][0]) + 2) + str(int(rDiagonal[i][1]) + 2)
                if num in player:
                    num = str(int(rDiagonal[i][0]) + 3) + str(int(rDiagonal[i][1]) + 3)
                    if num in player:
                        return "Player"
        #same for diagonals with negative slopes
        if lDiagonal[i] in player:
            num = str(int(lDiagonal[i][0]) + 1) + str(int(lDiagonal[i][1]) - 1)
            if num in player:
                num = str(int(lDiagonal[i][0]) + 2) + str(int(lDiagonal[i][1]) - 2)
                if num in player:
                    num = str(int(lDiagonal[i][0]) + 3) + str(int(lDiagonal[i][1]) - 3)
                    if num in player:
                        return "Player"
        #same but for computer
        if rDiagonal[i] in computer:
            num = str(int(rDiagonal[i][0]) + 1) + str(int(rDiagonal[i][1]) + 1)
            if num in computer:
                num = str(int(rDiagonal[i][0]) + 2) + str(int(rDiagonal[i][1]) + 2)
                if num in computer:
                    num = str(int(rDiagonal[i][0]) + 3) + str(int(rDiagonal[i][1]) + 3)
                    if num in computer:
                        return "Computer"
        if lDiagonal[i] in computer:
            num = str(int(lDiagonal[i][0]) + 1) + str(int(lDiagonal[i][1]) - 1)
            if num in computer:
                num = str(int(lDiagonal[i][0]) + 2) + str(int(lDiagonal[i][1]) - 2)
                if num in computer:
                    num = str(int(lDiagonal[i][0]) + 3) + str(int(lDiagonal[i][1]) - 3)
                    if num in computer:
                        return "Computer"
    
    #for diagonal that can be either of positive or negative slopes
    for i in range(len(diagonal)):
        if diagonal[i] in player:
            num = str(int(diagonal[i][0]) + 1) + str(int(diagonal[i][1]) + 1)
            if num in player:
                num = str(int(diagonal[i][0]) + 2) + str(int(diagonal[i][1]) + 2)
                if num in player:
                    num = str(int(diagonal[i][0]) + 3) + str(int(diagonal[i][1]) + 3)
                    if num in player:
                        return "Player"
        if diagonal[i] in player:
            num = str(int(diagonal[i][0]) + 1) + str(int(diagonal[i][1]) - 1)
            if num in player:
                num = str(int(diagonal[i][0]) + 2) + str(int(diagonal[i][1]) - 2)
                if num in player:
                    num = str(int(diagonal[i][0]) + 3) + str(int(diagonal[i][1]) - 3)
                    if num in player:
                        return "Player"
        if diagonal[i] in computer:
            num = str(int(diagonal[i][0]) + 1) + str(int(diagonal[i][1]) + 1)
            if num in computer:
                num = str(int(diagonal[i][0]) + 2) + str(int(diagonal[i][1]) + 2)
                if num in computer:
                    num = str(int(diagonal[i][0]) + 3) + str(int(diagonal[i][1]) + 3)
                    if num in computer:
                        return "Computer"
        if diagonal[i] in computer:
            num = str(int(diagonal[i][0]) + 1) + str(int(diagonal[i][1]) - 1)
            if num in computer:
                num = str(int(diagonal[i][0]) + 2) + str(int(diagonal[i][1]) - 2)
                if num in computer:
                    num = str(int(diagonal[i][0]) + 3) + str(int(diagonal[i][1]) - 3)
                    if num in computer:
                        return "Computer"
    
    return "None"

def checkWin(player):
    player = player.split(",")
    
    if len(player) < 4:
        return 0
    
    horizontalPlayer = sorted(player)  
    player.sort(key = sortVertical)
    
    for i in range(len(player)):
        try:
            if horizontalPlayer[i + 0][0] == horizontalPlayer[i + 1][0] == horizontalPlayer[i + 2][0] == horizontalPlayer[i + 3][0]:
                if (int(horizontalPlayer[i + 0][1]) - int(horizontalPlayer[i + 1][1]) == -1 and 
                    int(horizontalPlayer[i + 1][1]) - int(horizontalPlayer[i + 2][1]) == -1 and 
                    int(horizontalPlayer[i + 2][1]) - int(horizontalPlayer[i + 3][1]) == -1):
                    return 1
            if player[i + 0][1] == player[i + 1][1] == player[i + 2][1] == player[i + 3][1]:
                if (int(player[i + 0][0]) - int(player[i + 1][0]) == -1 and 
                    int(player[i + 1][0]) - int(player[i + 2][0]) == -1 and 
                    int(player[i + 2][0]) - int(player[i + 3][0]) == -1):
                    return 1
        except:
            break
    
    rDiagonal = ['11', '12', '13', '21', '22', '23', '31', '32', '33']
    lDiagonal = ['15', '16', '17', '25', '26', '27', '35', '36', '37']
    diagonal = ['14', '24', '34']

    for i in range(len(rDiagonal)):
        if rDiagonal[i] in player:
            num = str(int(rDiagonal[i][0]) + 1) + str(int(rDiagonal[i][1]) + 1)
            if num in player:
                num = str(int(rDiagonal[i][0]) + 2) + str(int(rDiagonal[i][1]) + 2)
                if num in player:
                    num = str(int(rDiagonal[i][0]) + 3) + str(int(rDiagonal[i][1]) + 3)
                    if num in player:
                        return 1
        if lDiagonal[i] in player:
            num = str(int(lDiagonal[i][0]) + 1) + str(int(lDiagonal[i][1]) - 1)
            if num in player:
                num = str(int(lDiagonal[i][0]) + 2) + str(int(lDiagonal[i][1]) - 2)
                if num in player:
                    num = str(int(lDiagonal[i][0]) + 3) + str(int(lDiagonal[i][1]) - 3)
                    if num in player:
                        return 1
        
    for i in range(len(diagonal)):
        if diagonal[i] in player:
            num = str(int(diagonal[i][0]) + 1) + str(int(diagonal[i][1]) + 1)
            if num in player:
                num = str(int(diagonal[i][0]) + 2) + str(int(diagonal[i][1]) + 2)
                if num in player:
                    num = str(int(diagonal[i][0]) + 3) + str(int(diagonal[i][1]) + 3)
                    if num in player:
                        return 1
        if diagonal[i] in player:
            num = str(int(diagonal[i][0]) + 1) + str(int(diagonal[i][1]) - 1)
            if num in player:
                num = str(int(diagonal[i][0]) + 2) + str(int(diagonal[i][1]) - 2)
                if num in player:
                    num = str(int(diagonal[i][0]) + 3) + str(int(diagonal[i][1]) - 3)
                    if num in player:
                        return 1
      
    return 0
 
def evaluate(computer_player, opponent):

    if checkWin(computer_player):
        return 1000000
    if checkWin(opponent):
        return -1000000

    board = [[0 for x in range(7)] for y in range(6)]
    boardV = [[0 for x in range(6)] for y in range(7)]
    computer_playerList = list(filter(None, computer_player.split(",")))
    opponentList = list(filter(None, opponent.split(",")))

    for i in range(len(computer_playerList)):
        board[6 - int(computer_playerList[i][0])][int(computer_playerList[i][1]) - 1] = 1
        boardV[int(computer_playerList[i][1]) - 1][int(computer_playerList[i][0]) - 1] = 1
    for i in range(len(opponentList)):
        board[6 - int(opponentList[i][0])][int(opponentList[i][1]) - 1] = -1
        boardV[int(opponentList[i][1]) - 1][int(opponentList[i][0]) - 1] = -1
    
    two = 0
    three = 0

    for i in range(6):
        flag = 0; before = 0; after = 0; temp = -1
        for j in range(7):
            if board[i][j] == 0 and flag < 2: before = before + 1; flag = 0
            elif j == 6 and board[i][j] == 0 and flag == 2:
                after = after + 1
                if before >= 2: two = two + 1
                if after >= 2: two = two + 1
                if after >= 1 and before >= 1: two = two + 1
            elif j == 6 and board[i][j] == 0 and flag == 3:
                after = after + 1
                if before >= 1: three = three + 1
                if after >= 1: three = three + 1
            elif board[i][j] == 0 and flag > 1: after = after + 1
            elif board[i][j] == 1 and after == 0: flag = flag + 1
            elif board[i][j] == 1 and after > 0 and flag == 2: 
                if after == 1: three = three + 1; flag = 1; before = 1; after = 0
                if before >= 2: two = two + 1
                if after >= 2: two = two + 1
                if after >= 1 and before >= 1: two = two + 1
                if before >= 2 or after >= 2 or (after >= 1 and before >= 1): 
                    flag = 1; before = after; after = 0
            elif board[i][j] == 1 and after > 0 and flag == 3: 
                if before >= 1: three = three + 1
                if after >= 1: three = three + 1
                if before >= 1 or after >= 1: 
                    flag = 1; before = after; after = 0
            elif board[i][j] == -1 and flag == 2:
                if before >= 2: two = two + 1
                if after >= 2: two = two + 1
                if after >= 1 and before >= 1: two = two + 1
                flag = 0; after = 0; before = 0
            elif board[i][j] == -1 and flag == 3:
                if before >= 1: three = three + 1
                if after >= 1: three = three + 1
                flag = 0; after = 0; before = 0
            elif board[i][j] == -1 and flag < 2:
                flag = 0
            else: flag = 0; after = 0; before = 0

    for i in range(7):
        flag = 0; before = 0; after = 0; temp = -1
        for j in range(6):
            if boardV[i][j] == 0 and flag < 2: before = before + 1; flag = 0
            elif j == 5 and boardV[i][j] == 0 and flag == 2:
                after = after + 1
                if before >= 2: two = two + 1
                if after >= 2: two = two + 1
                if after >= 1 and before >= 1: two = two + 1
            elif j == 5 and boardV[i][j] == 0 and flag == 3:
                after = after + 1
                if before >= 1: three = three + 1
                if after >= 1: three = three + 1
            elif boardV[i][j] == 0 and flag > 1: after = after + 1
            elif boardV[i][j] == 1 and after == 0: flag = flag + 1
            elif boardV[i][j] == 1 and after > 0 and flag == 2: 
                if after == 1: three = three + 1; flag = 1; before = 1; after = 0
                if before >= 2: two = two + 1
                if after >= 2: two = two + 1
                if after >= 1 and before >= 1: two = two + 1
                if before >= 2 or after >= 2 or (after >= 1 and before >= 1): 
                    flag = 1; before = after; after = 0
            elif boardV[i][j] == 1 and after > 0 and flag == 3: 
                if before >= 1: three = three + 1
                if after >= 1: three = three + 1
                if before >= 1 or after >= 1: 
                    flag = 1; before = after; after = 0
            elif boardV[i][j] == -1 and flag == 2:
                if before >= 2: two = two + 1
                if after >= 2: two = two + 1
                if after >= 1 and before >= 1: two = two + 1
                flag = 0; after = 0; before = 0
            elif boardV[i][j] == -1 and flag == 3:
                if before >= 1: three = three + 1
                if after >= 1: three = three + 1
                flag = 0; after = 0; before = 0
            elif boardV[i][j] == -1 and flag < 2:
                flag = 0
            else: flag = 0; after = 0; before = 0

    for k in range(3, 9):
        flag = 0; before = 0; after = 0; temp = -1
        for j in range(k + 1):
            i = k - j
            if i < 6 and j < 7:
                if board[i][j] == 0 and flag < 2: before = before + 1; flag = 0
                elif (j == 5) and board[i][j] == 0 and flag == 2:
                    after = after + 1
                    if before >= 2: two = two + 1
                    if after >= 2: two = two + 1
                    if after >= 1 and before >= 1: two = two + 1
                elif (j == 5) and board[i][j] == 0 and flag == 3:
                    after = after + 1
                    if before >= 1: three = three + 1
                    if after >= 1: three = three + 1
                elif board[i][j] == 0 and flag > 1: after = after + 1
                elif board[i][j] == 1 and after == 0: flag = flag + 1
                elif board[i][j] == 1 and after > 0 and flag == 2: 
                    if after == 1: three = three + 1; flag = 1; before = 1; after = 0
                    if before >= 2: two = two + 1
                    if after >= 2: two = two + 1
                    if after >= 1 and before >= 1: two = two + 1
                    if before >= 2 or after >= 2 or (after >= 1 and before >= 1): 
                        flag = 1; before = after; after = 0
                elif board[i][j] == 1 and after > 0 and flag == 3: 
                    if before >= 1: three = three + 1
                    if after >= 1: three = three + 1
                    if before >= 1 or after >= 1: 
                        flag = 1; before = after; after = 0
                elif board[i][j] == -1 and flag == 2:
                    if before >= 2: two = two + 1
                    if after >= 2: two = two + 1
                    if after >= 1 and before >= 1: two = two + 1
                    flag = 0; after = 0; before = 0
                elif board[i][j] == -1 and flag == 3:
                    if before >= 1: three = three + 1
                    if after >= 1: three = three + 1
                    flag = 0; after = 0; before = 0
                elif board[i][j] == -1 and flag < 2:
                    flag = 0
                else: flag = 0; after = 0; before = 0

    for k in range(2, -4, -1):
        for j in range(7):
            i = k + j
            if i > -1 and i < 6:
                if board[i][j] == 0 and flag < 2: before = before + 1; flag = 0
                elif (j == 5) and board[i][j] == 0 and flag == 2:
                    after = after + 1
                    if before >= 2: two = two + 1
                    if after >= 2: two = two + 1
                    if after >= 1 and before >= 1: two = two + 1
                elif (j == 5) and board[i][j] == 0 and flag == 3:
                    after = after + 1
                    if before >= 1: three = three + 1
                    if after >= 1: three = three + 1
                elif board[i][j] == 0 and flag > 1: after = after + 1
                elif board[i][j] == 1 and after == 0: flag = flag + 1
                elif board[i][j] == 1 and after > 0 and flag == 2: 
                    if after == 1: three = three + 1; flag = 1; before = 1; after = 0
                    if before >= 2: two = two + 1
                    if after >= 2: two = two + 1
                    if after >= 1 and before >= 1: two = two + 1
                    if before >= 2 or after >= 2 or (after >= 1 and before >= 1): 
                        flag = 1; before = after; after = 0
                elif board[i][j] == 1 and after > 0 and flag == 3: 
                    if before >= 1: three = three + 1
                    if after >= 1: three = three + 1
                    if before >= 1 or after >= 1: 
                        flag = 1; before = after; after = 0
                elif board[i][j] == -1 and flag == 2:
                    if before >= 2: two = two + 1
                    if after >= 2: two = two + 1
                    if after >= 1 and before >= 1: two = two + 1
                    flag = 0; after = 0; before = 0
                elif board[i][j] == -1 and flag == 3:
                    if before >= 1: three = three + 1
                    if after >= 1: three = three + 1
                    flag = 0; after = 0; before = 0
                elif board[i][j] == -1 and flag < 2:
                    flag = 0
                else: flag = 0; after = 0; before = 0

    return three * 20 + two * 5

def nextStates(state):
    nextStates = []
    flag = True
    for i in range(len(state)):
        stateNew = json.loads(json.dumps(state))
        if stateNew[i]['row'] == 6:
            if stateNew[i]['filled'] == True:
                continue
            else:
                stateNew[i]['filled'] = True
                nextStates.append(stateNew)
                flag = False
        else:
            stateNew[i]['row'] = stateNew[i]['row'] + 1
            nextStates.append(stateNew)
            flag = False
    return -1 if flag else nextStates

#takes a state as a string and parses it into a json
def parseStateString(state):
    states = []
    el = state.split(',')
    for i in range(len(el)):
        parts = el[i].split('-')
        states.append({"row": int(parts[0][0]), "col": int(parts[0][1]), "filled": parts[1] == "True"})
    return states

def nextStateString(state, player_computer):
    nextStatesString = []
    flag = True
    for i in range(len(state)):
        newPlayer_computer = player_computer
        if state[i]['filled'] == True and state[i]['row'] == 6:
            continue
        elif state[i]['filled'] == True:
            move = str(state[i]['row'] + 1) + str(i+1)
            if newPlayer_computer == '':
                newPlayer_computer = move
            else:
                newPlayer_computer = newPlayer_computer + ',' + move 
            nextStatesString.append(newPlayer_computer)
            flag = False
        else:
            move = str(state[i]['row']) + str(i+1)
            if newPlayer_computer == '':
                newPlayer_computer = move
            else:
                newPlayer_computer = newPlayer_computer + ',' + move
            nextStatesString.append(newPlayer_computer)              
            flag = False
    return -1 if flag else nextStatesString

def generateTree(state, level):
    turn = (state['turn'] + 1) % 2
    if level == 0:
        return
    nextSt = nextStates(state['state'])
    if nextSt == -1:
        return
    if turn:
        players = nextStateString(state['state'], state['player'])
    else:
        computers = nextStateString(state['state'], state['computer'])
    level = level - 1

    flagWin = False
    flagIndexWin = -1
    for i in range(len(nextSt)):
        if turn:
            if checkWin(players[i]):
                flagWin = True; flagIndexWin = i; break
        else:
            if checkWin(computers[i]):
                flagWin = True; flagIndexWin = i; break

    if flagWin:
        if turn:
            state['children'].append(
            {'state': nextSt[flagIndexWin], 
            'children': [], 
            'turn': turn, 
            'computer': state['computer'],
            'player': players[flagIndexWin]})
            return
        else:
            state['children'].append(
            {'state': nextSt[flagIndexWin], 
            'children': [], 
            'turn': turn, 
            'computer': computers[flagIndexWin],
            'player': state['player']})
            return

    for i in range(len(nextSt)):
        if turn:
            state['children'].append(
            {'state': nextSt[i], 
            'children': [], 
            'turn': turn, 
            'computer': state['computer'],
            'player': players[i]})
        else:
            state['children'].append(
            {'state': nextSt[i], 
            'children': [], 
            'turn': turn, 
            'computer': computers[i],
            'player': state['player']})
        
        generateTree(state['children'][i], level)

def minimax(position, depth, alpha, beta, maximizingPlayer, lvl, whoIsThePlayer):
    if depth == 0:
        computer = evaluate(position['computer'], position['player'])
        player = evaluate(position['player'], position['computer'])
        return (((100 * computer)) - ((200 * player)))

    if maximizingPlayer:
        maxEval = -10000000000
        j = -1
        for i in range(len(position['children'])):
            eval = minimax(position['children'][i], depth - 1, alpha, beta, False, lvl, whoIsThePlayer)
            if eval > alpha:
                j = i
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if depth == lvl: 
            moves = position['children'][j][whoIsThePlayer].split(",")
            return moves[len(moves) - 1]
        return maxEval
    else:
        minEval = +10000000000
        j = -1
        for i in range(len(position['children'])):
            eval = minimax(position['children'][i], depth - 1, alpha, beta, True, lvl, whoIsThePlayer)
            if eval < beta:
                j = i
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if depth == lvl: 
            moves = position['children'][j][whoIsThePlayer].split(",")
            return moves[len(moves) - 1]
        return minEval

def saveGame(name, state, BoardState, player, computer, flagPlayer, rows):
    with open(name + '.txt', 'w') as file:
        file.write(json.dumps(state))
        file.write('\n')
        file.write(json.dumps(BoardState))
        file.write('\n')
        file.write(json.dumps(player))
        file.write('\n')
        file.write(json.dumps(computer))
        file.write('\n')
        file.write(json.dumps(flagPlayer))
        file.write('\n')
        file.write(json.dumps(rows))

def loadsaveGame(name):
    with open(name + '.txt') as file:
        lines = []
        for i in file:
            lines.append(json.loads(i))
        state = lines[0]
        BoardState = lines[1]
        player = lines[2]
        computer = lines[3]
        flagPlayer = lines[4]
        rows = lines[5]
    return state, BoardState, player, computer, flagPlayer, rows

if __name__ == "__main__":
    state = parseStateString('11-False,12-False,13-False,14-False,15-False,16-False,17-False')
    BoardState = '11*-,12*-,13*-,14*-,15*-,16*-,17*-;21*-,22*-,23*-,24*-,25*-,26*-,27*-;31*-,32*-,33*-,34*-,35*-,36*-,37*-;41*-,42*-,43*-,44*-,45*-,46*-,47*-;51*-,52*-,53*-,54*-,55*-,56*-,57*-;61*-,62*-,63*-,64*-,65*-,66*-,67*-'
    player = ''
    computer = ''
    flagPlayer = 0
    rows = {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1}
    lvl = -1
    flagPlayer = -1
    while(lvl != 2 and lvl != 4 and lvl != 6):
        try:
            lvl = int(input("Enter game level from 1 to 3: ")) * 2
        except:
            print("Input not a number")
            input("Press any key to exit...")
            sys.exit()
    while(flagPlayer != 1 and flagPlayer != 0 and flagPlayer != 2):
        try:
            flagPlayer = int(input("Start First: 0, Start Second: 1, Load Game 2: "))
        except:
            print("Input not a number")
            input("Press any key to exit...")
            sys.exit()
    if flagPlayer == 2:
        name = input("Input save file name: ")
        try:
            state, BoardState, player, computer, flagPlayer, rows = loadsaveGame(name)
        except FileNotFoundError:
            print("File not found")
            input("Press any key to exit...")
            sys.exit()

    print("To save game enter 'save', to end the game enter 'end'")
    printBoard(BoardState)
    while 1:
        if flagPlayer == 0:
            col = input("Enter your move (col no.): ")
        else:
            states = {'state': json.loads(json.dumps(state)), 'children': [], 'turn': flagPlayer, 'player': player, 'computer': computer}
            generateTree(states, lvl)
            col = minimax(states, lvl, -10000000000, 10000000000, True, lvl, 'computer')[1]
        if col == 'end':
            break
        if col == 'save':
            name = input("Save game file name: ")
            saveGame(name, state, BoardState, player, computer, flagPlayer, rows)
            break
        try:
            if int(col) > 7 or rows[col] == 7:
                print("Move Not Available 1")
                printBoard(BoardState)
                continue
            move = str(rows[col]) + col
            if flagPlayer == 0:
                player, BoardState, state, flag = play(move, player, BoardState, state, flagPlayer)
            else:
                computer, BoardState, state, flag = play(move, computer, BoardState, state, flagPlayer)
            if not flag:
                print("Move Not Available")
                printBoard(BoardState)
            else:
                rows[col] = rows[col] + 1
                flagPlayer = (flagPlayer + 1) % 2
                printBoard(BoardState)
                winnner = checkIfWin(computer, player)
                if winnner == "Player":
                    print("You Won")
                    break
                elif winnner == "Computer":
                    print("You Lost")
                    break
        except ValueError:
            print(int(col), "Move Not Available")
            printBoard(BoardState)
    
    input("Press any key to exit...")
