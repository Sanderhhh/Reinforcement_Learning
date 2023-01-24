import learning_algorithm as algos
import chess
import chess.engine
import random

# TODO: set variable episode size.
def run_algorithm(useEngine = False):
    map = algos.Map('opponent_moves', useEngine)
    board = make_board('mate_in_three')
    print(board)
    iter = 0
    engine = None
    if useEngine == True:
        engine = chess.engine.SimpleEngine.popen_uci\
                (r"C:\Users\hofsa\Documents\stockfish_15.1_win_x64_popcnt\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe")
    while(iter != 1000 and not board.is_game_over()):
        print(iter)
        iter += 1
        for move in board.legal_moves:
            map.set_qvalue(board, move.uci())

        map.update_policy(board, board.legal_moves)
        bestMove = map.get_policy_move(board)
        bestMove_pushable = chess.Move.from_uci(bestMove)
        board = play_turn(board, bestMove_pushable, engine, useEngine)
        print(board)

def play_turn(board, move, engine, useEngine):
    board.push(move)
    blackMove = None
    if board.is_game_over():
        return board
    if useEngine:
        blackMove = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(blackMove.move)
    else:
        make_random_move(board)

    return board

def make_random_move(board):
    # take a random move
    moveNum = random.randint(0, board.legal_moves.count() - 1)
    print("Movenum = " + str(moveNum))
    num = 0
    for potential_move in board.legal_moves:
        if num == moveNum:
            blackMove = potential_move
            board.push(blackMove)
            print("MOVE PLAYED")
            break
        num += 1

def make_board(problem):
    if problem == "queen":
        return chess.Board('8/8/8/2k5/8/2K3Q1/8/8 w - - 0 1')
    elif problem == "rook":
        return chess.Board("8/8/8/2k5/8/6R1/3K4/8 w - - 0 1")
    elif problem == "testqueen":
        return chess.Board("8/8/8/2k5/8/2KQ4/8/8 w - - 0 1")
    elif problem == "mate_in_one":
        return chess.Board("1k6/8/1K6/1Q6/8/8/8/8 w - - 0 1")
    elif problem == "mate_in_two":
        return chess.Board("1k6/8/8/1KQ5/8/8/8/8 w - - 0 1")
    elif problem == "mate_in_three":
        return chess.Board("8/1k6/8/1K6/8/8/8/3Q4 w - - 2 2")
    else:
        return chess.Board('8/8/8/2k5/6R1/8/3K4/8 w - - 0 1')