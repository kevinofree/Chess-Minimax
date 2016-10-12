import chess

def recurse(board, depth):
    if depth == 1:
        print("Hey")
    else:
        move = list(board.legal_moves)[0]
        board.push(move)
        recurse(board, depth - 1)

def main():
    OG_board = chess.Board()
    print(OG_board)
    temp_board = chess.Board(OG_board.fen())
    print(OG_board)
    recurse(temp_board, 3)
    print(OG_board)

if __name__ == "__main__":
    main()


