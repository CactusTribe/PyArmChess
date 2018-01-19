import chess

def diff_between(board1, board2):
    old_position = None
    new_position = None

    for row in range(8):
        line_b1 = board1[row]
        line_b2 = board2[row]
        line_diff = [(str(chr(97 + col)), 8-row) for col in range(len(line_b1)) if line_b1[col] != line_b2[col]]
        if line_diff != []:
            fst_diff = line_diff[0]
            if line_b2[ord(fst_diff[0])-97] == ".":
                old_position = "{}{}".format(fst_diff[0], fst_diff[1])
            else:
                new_position = "{}{}".format(fst_diff[0], fst_diff[1])

    return "{}{}".format(old_position, new_position)

def printBoard(board):
    for i, l in enumerate(board):
        print(8 - i, "|", ' '.join(l))

    print("  ", ''.join("-" * 16))
    print("   ", ' '.join("ABCDEFGH"))
    print("")

old_board_frame = [
"BBBBBBBB",
"BBBBBBBB",
"........",
"........",
"........",
"........",
"WWWWWWWW",
"WWWWWWWW"]

current_board_frame = [
"BBBBBBBB",
"BBBBBBBB",
"........",
"........",
"........",
".....W..",
"WWWWWWWW",
"WWWWWW.W"]

board = chess.Board()

next_move = diff_between( old_board_frame, current_board_frame )
print(next_move)

move = chess.Move.from_uci(next_move)
if move in board.legal_moves:
    board.push(move)
print(board)
