import sys, time
from vision.ChessCamera import ChessCamera
from vision.constants import *


def printBoard(board):
    for i, l in enumerate(board):
        print(8 - i, "|", ' '.join(l))

    print("  ", ''.join("-" * 16))
    print("   ", ' '.join("ABCDEFGH"))
    print("")


if __name__ == '__main__':
    if len(sys.argv) > 1:

        IMAGE_PATH = sys.argv[1]

        begin = time.time()
        print("# Camera init ...")
        ChessCamera = ChessCamera(IMAGE_PATH)
        print("> Done !", time.time() - begin, "sec")

        if "-c" in sys.argv:
            ChessCamera.calibration()
        else:
            if not DEBUG:
                last_valid_board = None
                valid_board = None
                old_boards = [None, None, None]

                while True:
                    current_board = ChessCamera.current_board_processed()

                    old_boards.pop(0)
                    old_boards.append(current_board)

                    if AVERAGE_BOARD:
                        if old_boards[2] == old_boards[1] and old_boards[1] == old_boards[0]:
                            last_valid_board = valid_board
                            valid_board = current_board

                    if valid_board != last_valid_board:
                        printBoard(valid_board)

            else:
                current_board = ChessCamera.current_board_processed()
                printBoard(current_board)

        # ChessCamera.camera.close()
    else:
        print("Usage: test <image> (options: -c calibration)")
