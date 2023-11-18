from collections import defaultdict
import chess
import chess.engine
import numpy as np
import random
import value_iteration

#def value_iteration:


# Q_learning class that contains formulas and parameters for the Q-learning algorithm
import run_algorithm

class Q_learning:
    def __init__(self, type = "q_learning"):
        self.alpha = 0.5
        self.gamma = 0.8
        self.type = type

    # Calculates the Q-value associated with a state-action pair
    def calculate_q(self, map, state, action, iteration):
        if self.type == "q_learning":
            return map.get_qvalue(state, action) + self.alpha * (map.get_state_reward(state, action, iteration) +
                                    (self.gamma * map.get_max_q_next_state(state, action)) - map.get_qvalue(state, action))
        if self.type == "SARSA":
            return map.get_qvalue(state, action) + self.alpha * (map.get_state_reward(state, action, iteration) +
                                (self.gamma * map.get_q_next_state_action(state, action)) - map.get_qvalue(state, action))

class Map:
    def __init__(self, iterations, epsilon = 0, reward_strategies = list('engine_eval'), useEngine = False, learning_type = 'q_learning'):
        self.algorithm = Q_learning(learning_type)          # Algorithm of our choosing
        self.epsilon = epsilon                              # Value for e-greedy, leave at 0 for greedy
        self.qvalues = defaultdict(dict)                    # Double-indexed dictionary with q-values for state-action pairs
        self.reward_strategies = reward_strategies          # Reward strategy list, "engine_eval", "opponent_moves", "piece_proximity", "is_check"
        # Chess engine that calculates the best moves and (optionally) state rewards
        self.useEngine = useEngine
        self.Engine = None
        self.iteration = 0
        self.checkmates_by_iteration = np.zeros(iterations, dtype = np.int8)
        if useEngine == True or reward_strategies[0] == 'engine_eval':
            self.engine = chess.engine.SimpleEngine.popen_uci\
                (r"C:\Users\hofsa\Documents\stockfish_15.1_win_x64_popcnt\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe")

    # function that gets the policy move without creating a seperate policy dictionary
    def get_best_move(self, board, legal_moves):
        bestMove = 0    # keeps track of the uci-string associated with the best move
        max = -100000         # value of the best move
        for move in legal_moves:        # loop through all the moves in a state and choose the best one
            try:
                # print("For the move " + move.uci() + ", the Q-value is: " + str(self.qvalues[board.unicode()][move.uci()]))
                if self.qvalues[board.unicode()][move.uci()] > max:
                    max = self.qvalues[board.unicode()][move.uci()]
                    bestMove = move.uci()
            except KeyError:
                self.qvalues[board.unicode()][move.uci()] = 0
                if self.qvalues[board.unicode()][move.uci()] > max:
                    max = self.qvalues[board.unicode()][move.uci()]
                    bestMove = move.uci()
        return bestMove

    def set_qvalue(self, state, action, iteration):
        # set the estimated value of a state.
        self.qvalues[state.unicode()][action] = self.algorithm.calculate_q(self, state, action, iteration)

    def get_qvalue(self, state, action):
        try:            # if the q-value exists, return it, otherwise set it to 0 and return that.
            return self.qvalues[state.unicode()][action]
        except KeyError:
            self.qvalues[state.unicode()][action] = 0
            return self.qvalues[state.unicode()][action]

    def get_max_q_next_state(self, state, action):
        # in order to get the max q-value for the next state, we have to simulate that the move is played, then
        # we have to predict the move that our opponent will take, using a random move.
        # lastly, we take the highest existing q-value that we have in that state.
        move_from_uci = chess.Move.from_uci(action)
        board2 = chess.Board(state.fen())
        board2.push(move_from_uci)
        max_q = -1000
        if board2.legal_moves.count()==0:
            return 0
        black_move = self.engine.play(board2, chess.engine.Limit(time=0.001))
        board2.push(black_move.move)
        for white_move in board2.legal_moves:
            try:
                if self.qvalues[board2.unicode()][white_move.uci()] >= max_q:
                    # if the max q is higher store that value
                    max_q = self.qvalues[board2.unicode()][white_move.uci()]
            except KeyError:
                self.qvalues[board2.unicode()][white_move.uci()] = 0
                if self.qvalues[board2.unicode()][white_move.uci()] >= max_q:
                    # if the max q is higher store that value
                    max_q = self.qvalues[board2.unicode()][white_move.uci()]
        board2.pop()
        return max_q

    def get_q_next_state_action(self, state, action):
        move_from_uci = chess.Move.from_uci(action)
        board2 = chess.Board(state.fen())
        board2.push(move_from_uci)
        for move in board2.legal_moves:
            board2.push(move)
            try:
                move = self.e_greedy(board2)
                return self.qvalues[board2.fen()][move]
            except KeyError:
                # if there is no entry for the policy, return 0
                return 0
        return 0

    def e_greedy(self, board):
        num = random.uniform(0,1)
        if num < self.epsilon and board.legal_moves.count() > 1:
            # return a random move if value unnder epsilon
            moveNum = random.randint(0, board.legal_moves.count() - 1)
            return list(board.legal_moves)[moveNum].uci()
        else:
            return self.get_best_move(board, board.legal_moves)

    def get_state_reward(self, state, action, iteration):
        score = 0                                       # variable to keep track of the state reward
        action_pushable = chess.Move.from_uci(action)   # push the action, so that we get the reward of the resulting state
        state.push(action_pushable)
        if state.is_game_over():                        # if the game is over, return the max reward, but only if we win
            if state.is_checkmate():
                self.epsilon = self.epsilon - 1.0/1000
                if self.epsilon < 0.01:
                    self.epsilon = 0.01
                print("Checkmate at iteration " + str(iteration))
                if iteration > 0:
                    self.checkmates_by_iteration[iteration] += 1
                score = 1000
            else:
                score = -10
            state.pop()
            return score
        """
        for strategy in self.reward_strategies:
            # if the reward strategy is engine evaluation, let the engine analyze the position, and use that to calculate the reward
            if strategy == 'engine_eval':
                # simulate the action that our opponent will take, given our action
                blackMove = self.engine.play(state, chess.engine.Limit(time=0.1))
                state.push(blackMove.move)
                evaluation = self.engine.analyse(state, chess.engine.Limit(time = 0.1))
                score = evaluation['score'].white()
                if isinstance(score, chess.engine.Mate):    # if the score is presented as a mate in x, convert it to an integer
                    score = score.score(mate_score = 2)
                # if the score is presented as centipawns, apply division such that it is smaller than mating scores
                if isinstance(score, chess.engine.Cp):
                    score = score.score()/1000 - 10
                state.pop()     # undo the simulated moves
            
            if strategy == 'opponent_moves':
                score += 8 - state.legal_moves.count()
            if strategy == 'is_check':
                score += int(state.is_check())
            if strategy == 'piece_proximity':
                black_king = state.king(chess.BLACK)
                point_a = chess.parse_square(action[0:2])
                point_b = chess.parse_square(action[2:4])
                if chess.square_distance(black_king, point_a) < chess.square_distance(black_king, point_b):
                    score -= 0.1
            if strategy == 'king_proximity':
                black_king = state.king(chess.BLACK)
                point_a = chess.parse_square(action[0:2])
                point_b = chess.parse_square(action[2:4])
                if point_b == state.king(chess.WHITE):
                    if chess.square_distance(black_king, point_a) > chess.square_distance(black_king, point_b):
                        print("KING PROXIMITY: " + action)
                        score += chess.square_distance(black_king, point_a) - chess.square_distance(black_king, point_b)
            if strategy == 'blunder_queen':
                white_king = state.king(chess.WHITE)
                white_pieces = state.pieces(chess.QUEEN, chess.WHITE)
                white_queen = white_pieces.pop()
                black_king = state.king(chess.BLACK)
                if chess.square_distance(black_king, white_queen) == 1 \
                        and chess.square_distance(white_queen, white_king) > 1:
                    score = -1.1
            if strategy == 'push_to_wall':
                for move in state.legal_moves:
                    beginning_uci = (move.uci())[0:2]
                    destination_uci = (move.uci())[2:4]
                    beginning = chess.parse_square(beginning_uci)
                    destination = chess.parse_square(destination_uci)
                    corner = chess.parse_square('h1')
                    if chess.square_distance(beginning, corner) > \
                            chess.square_distance(destination, corner):
                        score -= 1
            if strategy == 'timer':
                score -= 1
            """

        state.pop()
        return score -1

    def get_checkmate_list(self):
        return self.checkmates_by_iteration