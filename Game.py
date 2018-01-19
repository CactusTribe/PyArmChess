import chess, sys, time

from vision.ChessCamera import ChessCamera
from vision.constants import *

default_board = [
"BBBBBBBB",
"BBBBBBBB",
"........",
"........",
"........",
"........",
"WWWWWWWW",
"WWWWWWWW"]

class Game():

    def __init__(self):
        self.board = None
        self.next_move = None

    def new_game(self):
        print("-> Create chessboard...")
        self.board = chess.Board()


    def detect_next_move(self, board1, board2):
        if board1 == None or board2 == None: return ""

        old_position = None
        new_position = None

        print("-> Compute next move...")
        for row in range(8):
            line_b1 = "".join(board1[row])
            line_b2 = "".join(board2[row])
            line_diff = [(str(chr(97 + col)), 8-row) for col in range(len(line_b1)) if line_b1[col] != line_b2[col]]
            if line_diff != []:
                fst_diff = line_diff[0]
                if line_b2[ord(fst_diff[0])-97] == ".":
                    old_position = "{}{}".format(fst_diff[0], fst_diff[1])
                else:
                    new_position = "{}{}".format(fst_diff[0], fst_diff[1])

        self.next_move = "{}{}".format(old_position, new_position)

    def apply_next_move(self):
        try:
            move = chess.Move.from_uci(self.next_move)
            if move in self.board.legal_moves:
                self.board.push(move)

        except:
            print("# Illegal moves.")


def printBoard(board):
    str_board = str(board)
    list_board = [str_board[i:i+16].strip("\n").replace(" ","") for i in range(0, len(str_board), 16)]

    for i, l in enumerate(list_board):
        print(8 - i, "|", ' '.join(l))

    print("  ", ''.join("-" * 16))
    print("   ", ' '.join("ABCDEFGH"))
    print("")

def boardToList(board):
    str_board = str(board)
    list_board = [str_board[i:i+16].strip("\n").replace(" ","") for i in range(0, len(str_board), 16)]
    return list_board

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Usage: Game.py")
        sys.exit(1)

    IMAGE_PATH = "vision/samples/begin.jpg"

    ChessGame = Game()
    ChessCamera = ChessCamera(IMAGE_PATH)

    ChessGame.new_game()
    printBoard(ChessGame.board)

    valid_board = default_board
    last_valid_board = default_board
    old_boards = [None, None, None]

    while True:
        current_board = ChessCamera.current_board_processed()
        old_boards.pop(0)
        old_boards.append(current_board)

        if AVERAGE_BOARD:
            if old_boards[0] == old_boards[1] and old_boards[1] == old_boards[2]:
                last_valid_board = valid_board
                valid_board = current_board

        else:
            last_valid_board = valid_board
            valid_board = current_board

        if valid_board != last_valid_board:
            ChessGame.detect_next_move( last_valid_board, valid_board )
            print(" #", ChessGame.next_move)

            ChessGame.apply_next_move()
            printBoard(ChessGame.board)

        time.sleep(1)
