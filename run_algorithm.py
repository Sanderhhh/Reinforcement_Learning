import learning_algorithm as algos
import chess
import chess.engine
import random

def run_algorithm(useEngine = True, problem_type = 'queen', depth = 8, imitation_iterations = 15, iterations = 3000):
    reward_strategies = ['timer']
    map = algos.Map(iterations, 0.2, reward_strategies, useEngine, 'SARSA')
    moves, game_total, imitation_games = 0, 0, 0
    engine = None
    if useEngine == True:
        engine = chess.engine.SimpleEngine.popen_uci\
                (r"C:\Users\hofsa\Documents\stockfish_15.1_win_x64_popcnt\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe")
    while(imitation_games < imitation_iterations):
        imitation_games += 1
        board = make_board(problem_type)
        imitation_learning(board, map, engine, depth)
    while(game_total != iterations):
        moves = 0
        board = make_board(problem_type)
        # print("Starting game number " + str(game_total))
        while(moves != depth and not board.is_game_over()):
            moves += 1
            move = map.e_greedy(board)
            #for move in board.legal_moves:
            map.set_qvalue(board, move, game_total)
            try:
                #bestMove = map.e_greedy(board)
                bestMove_pushable = chess.Move.from_uci(move)
                board = play_turn(board, bestMove_pushable, engine, False)
                # board.push(bestMove_pushable)
            except TypeError:       # case where we analyze board with no legal moves
                break
        game_total += 1
    # optimal_play_sequence(board, map, engine, useEngine)
    return map.get_checkmate_list()

def play_turn(board, move, engine, useEngine):
    board.push(move)
    blackMove = None
    if board.is_game_over():
        return board
    if useEngine:
        blackMove = engine.play(board, chess.engine.Limit(time=0.01))
        board.push(blackMove.move)
    else:
        make_random_move(board)
    return board

def make_random_candidate(board):
    # take a random move
    moveNum = random.randint(0, board.legal_moves.count() - 1)
    num = 0
    for potential_move in board.legal_moves:
        if num == moveNum:
            return potential_move
        num += 1

def make_random_move(board):
    # take a random move
    moveNum = random.randint(0, board.legal_moves.count() - 1)
    num = 0
    for potential_move in board.legal_moves:
        if num == moveNum:
            blackMove = potential_move
            board.push(blackMove)
            break
        num += 1

def optimal_play_sequence(board, map, engine, useEngine):
    print("Learning is finished. The optimal sequence of play is as follows: ")
    move_count = 0
    while board.is_game_over and move_count < 30:
        move_count += 1
        print(board)
        print()
        try:
            bestMove = map.get_best_move(board)
            bestMove_pushable = chess.Move.from_uci(bestMove)
            board = play_turn(board, bestMove_pushable, engine, useEngine)
            # board.push(bestMove_pushable)
        except TypeError:
            break

def imitation_learning(board, map, engine, depth):
    moveCounter = 0
    while not board.is_game_over() and moveCounter != depth:
        moveCounter += 1
        # print(board)
        move = engine.play(board, chess.engine.Limit(time = 1))
        # print("Best move: " + move.move.uci())
        map.set_qvalue(board, move.move.uci(), 0)
        play_turn(board, move.move, engine, True)

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