from collections import defaultdict
import chess
import chess.engine

# TODO: implement TD learning and possibly other algorithms
# Q_learning class that contains formulas and parameters for the Q-learning algorithm
class Q_learning:
    def __init__(self):
        self.alpha = 0.5
        self.gamma = 0.8

    # Calculates the Q-value associated with a state-action pair
    def calculate_q(self, map, state, action):
        return map.get_qvalue(state, action) + self.alpha * (map.get_state_reward(state, action) +
                                    (self.gamma * map.get_max_q_next_state(state, action)) - map.get_qvalue(state, action))

class Map:
    def __init__(self, reward_strategy = 'engine_eval', useEngine = 'True'):
        self.algorithm = Q_learning()           # Algorithm of our choosing
        self.policy = defaultdict(dict)         # Dictionary of best move per state
        self.qvalues = defaultdict(dict)        # Double-indexed dictionary with q-values for state-action pairs
        self.reward_strategy = reward_strategy    # Reward strategy
        # Chess engine that calculates the best moves and (optionally) state rewards
        self.useEngine = useEngine
        self.Engine = None
        if useEngine == True or reward_strategy == 'engine_eval':
            self.engine = chess.engine.SimpleEngine.popen_uci\
                (r"C:\Users\hofsa\Documents\stockfish_15.1_win_x64_popcnt\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe")

    def update_policy(self, board, legal_moves):
        bestMove = 0    # keeps track of the uci-string associated with the best move
        max = 0         # value of the best move
        for move in legal_moves:        # loop through all the moves in a state and choose the best one
            print("For the move " + move.uci() + ", the Q-value is: " + str(self.qvalues[board.fen()][move.uci()]))
            if self.qvalues[board.fen()][move.uci()] >= max:
                max = self.qvalues[board.fen()][move.uci()]
                bestMove = move.uci()
        self.policy[board.fen()] = bestMove     # set the policy to the best move

    def set_qvalue(self, state, action):
        # set the estimated value of a state.
        self.qvalues[state.fen()][action] = self.algorithm.calculate_q(self, state, action)

    def get_qvalue(self, state, action):
        try:            # if the q-value exists, return it, otherwise set it to 0 and return that.
            return self.qvalues[state.fen()][action]
        except KeyError:
            self.qvalues[state.fen()][action] = 0
            return self.qvalues[state.fen()][action]

    def get_max_q_next_state(self, state, action):
        # in order to get the max q-value for the next state, we have to simulate that the move is played, then
        # we have to predict the move that our opponent will take, using a random move.
        # lastly, we take the highest existing q-value that we have in that state.
        move_from_uci = chess.Move.from_uci(action)
        board2 = chess.Board(state.fen())
        board2.push(move_from_uci)
        for move in board2.legal_moves:
            board2.push(move)
            for moremoves in board2.legal_moves:
                try:
                    qval = self.qvalues[board2.fen()][moremoves.uci()]
                    return qval
                except KeyError:
                    self.qvalues[board2.fen()][moremoves.uci()] = 0
            board2.pop()
        return 0

    # TODO: add more state reward strategies
    def get_state_reward(self, state, action):
        score = 0                                       # variable to keep track of the state reward
        action_pushable = chess.Move.from_uci(action)   # push the action, so that we get the reward of the resulting state
        state.push(action_pushable)
        if state.is_game_over():                        # if the game is over, return the max reward, but only if we win
            if state.is_checkmate():
                score = 100
            else:
                score = 0
            state.pop()
            return score
        # if the reward strategy is engine evaluation, let the engine analyze the position, and use that to calculate the reward
        if self.reward_strategy == 'engine_eval':
            # simulate the action that our opponent will take, given our action
            blackMove = self.engine.play(state, chess.engine.Limit(time=0.1))
            state.push(blackMove.move)
            evaluation = self.engine.analyse(state, chess.engine.Limit(time = 0.1))
            score = evaluation['score'].white()
            if isinstance(score, chess.engine.Mate):    # if the score is presented as a mate in x, convert it to an integer
                score = score.score(mate_score = 100)
            # if the score is presented as centipawns, apply division such that it is smaller than mating scores
            if isinstance(score, chess.engine.Cp):
                score = score.score()/1000
            state.pop()     # undo the simulated moves
        if self.reward_strategy == 'opponent_moves':
            legal_moves_black = state.legal_moves.count()
            score = 8 - legal_moves_black
        state.pop()
        print("Score for the move " + action + ": " + str(score))
        return score

    def get_policy_move(self, board):
        return self.policy[board.fen()]
