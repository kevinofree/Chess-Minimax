import chess
from IPython.display import display

def heuristicX():
#Heuristic function for PlayerX
    pass

def heuristicY():
#Heuristic function for PlayerY
    pass

def updateBoard(board,move):
# generate list of possible moves by opponent
# finds correct move and updates board 
    l = [] 
    for i in board.legal_moves:     # generate moves
        if str(i)[-2:] == str(move)[-2:]:
            l.append(str(i))

    for i in l:
        index = getIndex(i[:2])
        if board.piece_at(index) == str(move)[4]:
            board.push(i)
            return


def getIndex(move):
# Returns an index given a square on the board
    d = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    index = d[move[0]] + 7 * (int(move[1]) -1)
    return index

def showMove(turn, move, board):
# Displays the board 
# Writes move to appropriate log file
    print(str(board)) # print the board in ascii
    board.pop()       
    index = getIndex(str(move)[:2])
    piece = board.piece_at(index)
    board.push(move)
    if board.turn == False: 
        log_x = open('log_x.txt','a')
        log_x.write(str(turn) +':X' +':' + str(piece) +':'+ str(move)[-2:]+ '\n')
        log_x.close()
    else:                   
        log_y = open('log_y.txt','a')
        log_y.write(str(turn) +':Y' +':' + str(piece) +':'+ str(move)[-2:]+ '\n')
        log_y.close()

def move(board):
# Makes a move for each player
    move = list(board.legal_moves)[0]
    board.push(move)
    return move

def lastMoveMade(fn):
# Returns the last entry in log file 
    with open(fn) as fh:
        moveList = fh.readlines()
    fh.close()
    if moveList == []:
        return ''
    else:
        return moveList[-1]

def setupBoard():
# Setup initial board for both players
# PlayerX starts first and has a rook, knight, and king
# PlayerY has a king and knight
    return chess.Board("1n2k3/8/8/8/8/8/8/R3K1N1 w KQkq - 0 4")

def play(n):
# Driver function which initiates play
# input: number of moves n
    player = input("Pick your player (X or Y):")
    board = setupBoard()
    log_x = open('log_x.txt','w+')
    log_y = open('log_y.txt','w+')
    log_x.close()
    log_y.close()
    xMove = ''  
    yMove = ''
    turnCount = 1

    if player.upper() == 'X': # PlayerX (white) was chosen
        while turnCount != n or board.is_game_over() != True:
            if turnCount is 1:
                print("First move of the game")
                nextMove = move(board)
                showMove(turnCount, nextMove, board)
                turnCount +=1
            else:
                while yMove == lastMoveMade('log_y.txt'): # Wait for PlayerY to make a move
                    pass
                print("current turn is ", board.turn)
                yMove = lastMoveMade('log_y.txt') # Change last move made by PlayerY
                updateBoard(board,yMove)     # Update board with most recent move
                nextMove = move(board)
                showMove(turnCount, nextMove, board)
                turnCount += 1

    elif player.upper() == 'Y': # PlayerY (black) was chosen
        while turnCount != n or board.is_game_over() != True:
            while xMove == lastMoveMade('log_x.txt'): # Wait for PlayerX to make a move
                pass
            xMove = lastMoveMade('log_x.txt') # Change last move made by PlayerX
            updateBoard(board,xMove)     # Update board with most recent move
            nextMove = move(board)      
            showMove(turnCount,nextMove,board)
            turnCount+=1
    else:
        print("That player does not exist")


def main():
    maxMoves = input("Input the max number of turns: ")
    print("Turn limit set to: ", maxMoves)
    play(maxMoves)

if __name__ == "__main__":
    main()
