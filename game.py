import chess
from IPython.display import display

def heuristicX():
"""
Heuristic function for PlayerX
""""

def heuristicY():
"""
Heuristic function for PlayerY
""""

def lastMoveFromFile(fn):
    with open(fn) as fh:
        moveList = fh.readlines()
    fh.close()
    if moveList == []:
        return ''
    else:
        return moveList[-1]
    
def move(board):
# makes a move for each player
    move = list(board.legal_moves)[0]
    board.push(move)
    return move

def showMove(move, board):
    print(str(board)) # change this to svg display
    if board.turn == False:  # Player X's turn 
        log_x = open('log_x.txt', 'a')
        log_x.write(str(move)+'\n')
        log_x.close()
    else:                    # Player Y's turn
        log_y = open('log_y.txt', 'a')
        log_y.write(str(move)+'\n')
        log_y.close()
        
def play(n):
#Driver function which initiates play
#input: number of plays n
    turnCount = n
    board = setupBoard()
    board.turn = True
    log_x = open('log_x.txt', 'w+')
    log_x.close()
    log_y = open('log_y.txt', 'w+')
    log_y.close()
    lastMoveX = lastMoveFromFile('log_x.txt')
    lastMoveY = lastMoveFromFile('log_y.txt')
    print("Entering Game Loop")

    while turnCount != 0 or board.is_game_over() != False:
        if board.turn == True: # Player X's turn
            if turnCount == n: # first move of game dont check file
                print("First move of game")
                nextMove = move(board)
                showMove(nextMove, board)
                board.turn = False
            else: # wait for PlayerY to change log file
                print("Waiting for PlayerY to move")
                newLastMove = lastMoveFromFile('log_y.txt')
                while lastMoveY == newLastMove: # wait for PLayerY to make a move
                    pass
                lastMoveY = newLastMove         # update last PlayerY move
                nextMove = move(board)
                showMove(nextMove, board)     
                board.turn = False   
        else:   # Wait for PlayerX to change log file
            newLastMove = lastMoveFromFile('log_x.txt')
            print(newLastMove)
            print("Waiting for PlayerX to move")
            while lastMoveX == newLastMove:     # wait for PLayerX to make a move
                pass
            lastMoveX = newLastMove         # update last PlayerX move
            nextMove = move(board)
            showMove(nextMove,board)
            board.turn = True
        turnCount-=1

def setupBoard():
"""
Setup intial board for both players
PlayerX has a rook, knight, and king
PlayerY has a king and knight
"""
    return chess.Board("1n2k3/8/8/8/8/8/8/R3K1N1 b KQkq - 0 4")

def main():
    maxTurn = 10
    print('Turn limit is set to', maxTurn)
    play(maxTurn)
    print("Game Over")

if __name__ == "__main__":
    main()
