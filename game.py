import chess
from IPython.display import display

def play(n):
"""
Driver function which initiates play
input: number of plays n
""""

def heuristicX():
"""
Heuristic function for PlayerX
""""

def heuristicY():
"""
Heuristic function for PlayerY
""""

def move():
"""
Makes a move
"""

def showMove():
"""
Display the move visually 
Logs the move in the appropriate file
"""

def setupBoard():
"""
Setup intial board for both players
PlayerX has a rook, knight, and king
PlayerY has a king and knight
"""
    return chess.Board("1n2k3/8/8/8/8/8/8/R3K1N1 b KQkq - 0 4")

def main():
    board = setupBoard()

if __name__ == "__main__":
    main()