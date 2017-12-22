import sys
from ChessCamera import ChessCamera

def printBoard(board):
    for i, l in enumerate(board):
        print(8-i,"|", ' '.join(l))

    print("  ",''.join("-"*16))
    print("   ",' '.join("ABCDEFGH"))

if __name__ == '__main__':
    if len(sys.argv) > 1:

        IMAGE_PATH = sys.argv[1]
        ChessCamera = ChessCamera(IMAGE_PATH)

        if "-c" in sys.argv:
            ChessCamera.calibration()
        else:
            current_board = ChessCamera.current_board_processed()
            printBoard(current_board)
    else:
        print("Usage: test <image> (options: -c calibration)")
