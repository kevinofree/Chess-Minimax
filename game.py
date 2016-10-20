import chess
from IPython.display import display, clear_output
from random import randint
import sys

def heuristicX(board):
#Heuristic function for PlayerX
    piece_value = {'n':3, 'N' :3, 'k':6.5, 'K' :6.5, 'R': 5}
    white_weight, black_weight  = 0, 0
    white_pieces, black_pieces = 0, 0
    check_board = str(board)
    for piece in check_board:
        if piece.islower():
            black_pieces = black_pieces + 1
            black_weight += piece_value[piece]
        if piece.isupper():
            white_pieces = white_pieces + 1
            white_weight += piece_value[piece]
    if board.turn == True:
        score = (len(list(board.legal_moves)) + (white_pieces - black_pieces)) * white_weight
    else:
        score = ( len(list(board.legal_moves)) + (black_pieces - white_pieces)) * black_weight
    return score

def heuristicY(board):
#Heuristic function for PlayerY
    piece_amt = {'n':0, 'N' :0, 'k':0, 'K' :0, 'R': 0, 'r' : 0}
    score = 0
    check_board = str(board)
    for piece in check_board:
        if piece in piece_amt:
            piece_amt[piece] += 1
    score = ( 200*(piece_amt['k'] - piece_amt['K'])  
            + 5*(piece_amt['r'] - piece_amt['R']) 
            + 3*(piece_amt['n'] - piece_amt['N']) 
            + 0.1*(len(list(board.legal_moves))) )
    return score

def minimax(board, depth, alpha, beta):
    if depth == 0:
        if board.turn == True:
            return (heuristicX(board), None)
        else:
            return (heuristicY(board), None)
    else:
        if board.turn == True:
            bestmove = None
            for move in list(board.legal_moves):
                temp_board = chess.Board(board.fen())
                temp_board.push(move)
                score, _move = minimax(temp_board, depth - 1, alpha, beta)
                if score > alpha:
                    alpha = score
                    if alpha >= beta:
                        break
                    bestmove = move
            return (alpha, bestmove)
        else:
            bestmove = None
            for move in list(board.legal_moves):
                temp_board = chess.Board(board.fen())
                temp_board.push(move)
                score, _move = minimax(temp_board, depth - 1, alpha, beta)
                if score < beta:
                    beta  = score
                    bestmove = move
                    if alpha >= beta:
                        break
            return (beta, bestmove)

def updateBoard(board,move):
# Updates the board after the opponent has made a move
    move = move.split(':')
    sanmove = move[1].upper() + move[2] #must be upper to be valid
    matched_move = move[1]+move[2]
    board.push_san(sanmove)

def getIndex(move):
# Returns an index given a square on the board
    d = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    index = d[move[0]] + 8 * (int(move[1])-1)
    return index

def showMove(turn, move, oldmove, board):
    # Displays the board 
    # Writes move to appropriate log file
    clear_output()
    display(board)
    board.pop()       # go back one move
    mv = str(move)[:2] 
    index = getIndex(mv) # find the character of the piece moved
    piece = board.piece_at(index)
    board.push(move)    # return to current board
    if board.turn == False: 
        log_x = open('log_x.txt','a')
        if turn != 1:
            oldmove = oldmove.split(' ')
            oldmove = str(turn-1) + ' '+ oldmove[1]
            log_x.write(oldmove)
        log_x.write(str(turn) +' X:' + str(piece) +':'+ str(move)[-2:]+ '\n')
        log_x.close()
    else:                   
        log_y = open('log_y.txt','a')
        oldmove = oldmove.split(' ')
        oldmove = str(turn) + ' '+ oldmove[1]
        log_y.write(oldmove)
        log_y.write(str(turn+1) +' Y:' + str(piece).lower() +':'+ str(move)[-2:]+ '\n')
        log_y.close()

def move(board):
# Makes a move for each player
    temp_board = chess.Board(board.fen())
    move = minimax(temp_board, 5, float('-inf'), float('inf'))[1]
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
        if moveList[-1] == "Checkmate\n" or moveList[-1] == "Stalemate\n":
            sys.exit(0)
        return moveList[-1]

def setupBoard():
# Setup initial board for both players
# PlayerX starts first and has a rook, knight, and king
# PlayerY has a king and knight
    return chess.Board("2n1k3/8/8/8/8/8/8/4K1NR w KQkq - 0 4")

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
        while turnCount <= n*2:
            if board.is_checkmate() or board.is_stalemate():
                if board.is_checkmate():
                    log_x = open('log_x.txt','a')
                    log_x.write("Checkmate\n")
                    log_x.close()
                    sys.exit(0)
                elif board.is_stalemate():
                    log_x = open('log_x.txt','a')
                    log_x.write("Stalemate\n")
                    log_x.close()
                    sys.exit(0)
                

            if turnCount is 1:
                nextMove = move(board)
                showMove(turnCount, nextMove, None, board)
            else:
                board.turn = False
                while yMove == lastMoveMade('log_y.txt'): # Wait for PlayerY to make a move
                    pass
                yMove = lastMoveMade('log_y.txt') # Change last move made by PlayerY)
                updateBoard(board,yMove)     # Update board with most recent move
                board.turn = True
                nextMove = move(board)           
                showMove(turnCount, nextMove, yMove, board )
            turnCount += 2

        log_x = open('log_x.txt','a')
        log_x.write("Maximum # of turns reached\n")
        log_x.close()

    elif player.upper() =="Y":
        xMove = ''
        while turnCount <= n*2:
            if board.is_checkmate() or board.is_stalemate():
                if board.is_checkmate() == True:
                    log_y = open('log_y.txt','a')
                    log_y.write("Checkmate\n")
                    log_y.close()
                    sys.exit(0)
                elif board.is_stalemate() == True:
                    log_y = open('log_y.txt','a')
                    log_y.write("Stalemate\n")
                    log_y.close()
                    sys.exit(0)
            else:
                board.turn = True
                while xMove == lastMoveMade('log_x.txt'):  # Wait for PlayerX to make a move
                    pass
                xMove = lastMoveMade('log_x.txt')   # Change last move made by PlayerY
                updateBoard(board,xMove)     # Update board with most recent move
                board.turn = False
                nextMove = move(board)   
                showMove(turnCount,nextMove, xMove, board)
                turnCount += 2

        log_y = open('log_y.txt','a')
        log_y.write("Maximum # of turns reached\n")
        log_y.close()
    else:
        print("That Player does not exist")

def main():
    maxMoves = int(input("Input the max number of turns:"))
    print('Turn limit set to:', maxMoves)
    play(maxMoves)

if __name__ == "__main__":
	main()
