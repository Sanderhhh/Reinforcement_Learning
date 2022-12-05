import random

class State():
    def __init__(self):
        self.bernoulli = False
        self.actions = []  # list of strings with action names
        self.rewards = []  # list of floating points with rewards
        self.transitions = []  # list of integers with the numbers of the states that can be moved to

    def execute_action(self, actionName):
        for index in self.actions:
            if (actionName == index):
                # if bernoulli variation of the problem, return 1 or 0, depending on the reward
                if self.bernoulli:
                    randomChance = random.uniform(0, 1)
                    if (randomChance < self.rewards[index]):
                        return self.rewards[index], self.transitions[index]
                    else:
                        return 0, self.transitions[index]
                else:
                    return self.rewards[index], self.transitions[index]
        return 0, 0  # return statement if the action name is invalid

    def set_action(self, actionName, actionReward, actionTransition):
        # set the names and values of the actions
        self.actions.append(actionName)
        self.rewards.append(actionReward)
        self.transitions.append(actionTransition)

    def get_actions(self):
        return self.actions  # return the list of action names

    def get_best_action(self):      # return the max of the rewards
        max = 0
        for idx, value in enumerate(self.rewards):
            if self.rewards[idx] >= self.rewards[max]:
                max = idx
        return max

class Map():
    def __init__(self):
        self.current_state = 0
        self.states = []

    def set_states(self, states):
        self.states.append(states)

    def execute_actions(self, index):
        reward, self.current_state = self.states[self.current_state].execute_action(index)
        return reward

    def get_actions(self):
        return self.states[self.current_state].get_actions()

    def get_current_best_action(self):
        # get the best action at the current state, so we can verify the algorithms effectiveness
        return self.states[self.current_state].get_best_action()