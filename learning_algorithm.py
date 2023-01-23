from collections import defaultdict
import chess
import chess.engine

class Q_learning:
    def __init__(self):
        self.alpha = 0.5
        self.gamma = 0.8

    def Q_learning(self, alpha = 0.5, gamma = 0.8):
        self.alpha = alpha
        self.gamma = gamma

    def calculate_q(self, map, state, action):
        return map.get_qvalue(state, action) + self.alpha * (map.get_state_reward(state) +
                                    self.gamma * map.get_max_q_next_state(state, action) - map.get_qvalue(state, action))

class Map:
    def __init__(self):
        self.qlearning = Q_learning()
        self.policy = defaultdict(dict)
        self.qvalues = defaultdict(dict)
        self.reward_strategy = 'engine_eval'
        self.engine = chess.engine.SimpleEngine.popen_uci\
            (r"C:\Users\hofsa\Documents\stockfish_15.1_win_x64_popcnt\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe")

    def get_qvalue(self, state, action):
        if not self.qvalues[state][action]:
            self.qvalues[state][action] = 0
        return self.qvalues[state][action]

    def get_max_q_next_state(self, state, action):
        return 0

    def get_state_reward(self, state):
        if self.reward_strategy == 'engine_eval':
            evaluation = self.engine.analyse(state, chess.engine.Limit(time = 0.1))
            score = evaluation['score'].white()
            if isinstance(score, chess.engine.Mate):
                score = score.score(mate_score = 100)
            if isinstance(score, chess.engine.Cp):
                score = score.score()/1000
            return score

    def set_qvalue(self, state, action):
        self.qvalues['state']['action'] = self.qlearning.calculate_q(self, state, action)
