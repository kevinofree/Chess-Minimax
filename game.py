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
    for i in list(board.legal_moves):     # generate moves
        if str(i)[2:] == str(move)[-3:-1]: # look for match of opponent's move
            index = getIndex(str(i)[:2])
            if str(board.piece_at(0)) == str(move)[4]:
                board.push(i)
                print("matched the move, " , str(i))
                break

def getIndex(move):
# Returns an index given a square on the board
    d = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    index = d[move[0]] + 8 * (int(move[1])-1)
    return index

def showMove(turn, move, board):
# Displays the board 
# Writes move to appropriate log file
    print(str(board)) # print the board in ascii
    board.pop()       # go back one move
    mv = str(move)[:2] 
    index = getIndex(mv) # find the character of the piece moved
    piece = board.piece_at(index)
    board.push(move)    # return to current board
    if board.turn == False: 
        log_x = open('log_x.txt','a')
        log_x.write(str(turn) +':X:' + str(piece) +':'+ str(move)[-2:]+ '\n')
        log_x.close()
    else:                   
        log_y = open('log_y.txt','a')
        log_y.write(str(turn) +':Y:' + str(piece).lower() +':'+ str(move)[-2:]+ '\n')
        log_y.close()

def move(board):
# Makes a move for each player
    move = list(board.legal_moves)[0]
    board.push(move)
    return move

def lastMoveMade(fn):
# Returns the last entry in log file 
    with open(fn) as log:
        moveList = log.readlines()
    log.close()
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
    player = str(input("Pick your player (X or Y): "))

    #setup and display initial board
    board = setupBoard()

    # Player X checks if log files exist, otherwise creates them
    if player.upper() == "X":
        log_x = open('log_x.txt','w+')
        log_y = open('log_y.txt','w+')
        log_x.close()
        log_y.close()

    turnCount = 1

    if player.upper() == "X":
        yMove = ''
        while turnCount <= n:
            print("Turn ", turnCount)
            if board.is_game_over() == True or board.is_stalemate() == True:
                break
            if turnCount is 1:
                nextMove = move(board)
                showMove(turnCount, nextMove,board)
            else:
                board.turn = False
                while yMove == lastMoveMade('log_y.txt'): # Wait for PlayerY to make a move
                    pass
                yMove = lastMoveMade('log_y.txt') # Change last move made by PlayerY)
                updateBoard(board,yMove)     # Update board with most recent move
                board.turn = True
                nextMove = move(board)           
                showMove(turnCount, nextMove, board)
            turnCount += 1
            
        if board.is_game_over() == True:
            log_x = open('log_x.txt','a')
            log_x.write("Checkmate\n")
        elif board.is_stalemate() == True:
            log_x = open('log_x.txt','a')
            log_x.write("Stalemate\n")
        else:
            log_x = open('log_x.txt','a')
            log_x.write("Maximum # of turns reached\n")

    elif player.upper() =="Y":
        xMove = ''
        while turnCount <= n:
            print("Turn ", turnCount)
            if board.is_game_over() == True or board.is_stalemate() == True:
                break
            board.turn = True
            while xMove == lastMoveMade('log_x.txt'):  # Wait for PlayerX to make a move
                pass
            xMove = lastMoveMade('log_x.txt')   # Change last move made by PlayerY
            updateBoard(board,xMove)     # Update board with most recent move
            board.turn = False
            nextMove = move(board)   
            showMove(turnCount,nextMove,board)
            turnCount += 1

        if board.is_game_over() == True:
            log_y = open('log_y.txt','a')
            log_y.write("Checkmate\n")
        elif board.is_stalemate() == True:
            log_y = open('log_y.txt','a')
            log_y.write("Stalemate\n")
        else:
            log_y = open('log_y.txt','a')
            log_y.write("Maximum # of turns reached\n")
    else:
        print("That Player does not exist")

def main():
    maxMoves = int(input("Input the max number turns:"))
    print('Turn limit set to:', maxMoves)
    play(maxMoves)

if __name__ == "__main__":
	main()
