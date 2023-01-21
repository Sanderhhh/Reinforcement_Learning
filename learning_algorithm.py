import defaultdict
import chess
import chess.engine

class q_learning:
    self.alpha = 0.5
    self.gamma = 0.8

    def q_learning(self, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

    def calculate_q(self, map, state, action):
        return map.get_qvalue(state, action) + alpha * (map.get_state_reward(state) +
                                    gamma * map.get_max_q_next_state(state, action) - map.get_qvalue(state, action))

class map:
    self.policy = defaultdict(dict)
    self.qvalues = defaultdict(dict)
    self.reward_strategy = 'engine_eval'
    self.engine = None

    def map(self, engine = None):
        self.engine = engine

    def get_qvalue(self, state, action):
        if not self.qvalues[state][action]:
            self.qvalues[state][action] = 0
        return self.qvalues[state][action]

    def get_state_reward(self, state):
        if self.reward_strategy == 'engine_eval':
            evaluation = engine.analyse(state, chess.engine.Limit(time = 0.1))
            wdl = evaluation['score']['wdl'].white()
            return wdl.winning_chance()

    def set_qvalue(self, state, action, q):
        self.qvalues['state']['action'] = q

