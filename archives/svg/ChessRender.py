import chess
import chess.svg

board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
print(board)

with open("board.svg", "w") as f:
    f.write(chess.svg.board(board=board, size=800, coordinates=False))
