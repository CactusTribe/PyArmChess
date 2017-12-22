import chess

board = chess.Board()

m1 = chess.Move.from_uci("e2e4")
board.push(m1)
print(board)
