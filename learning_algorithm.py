

class q_learning():
    self.policy = {}
    self.alpha = 0.5
    self.gamma = 0.8

    def calculate_q(self, state, action):
        return state.qvalue(action) + alpha * (state.reward() + state.max_q_next_state(action) - state.qvalue(action))
