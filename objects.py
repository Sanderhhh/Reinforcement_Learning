import numpy

class State():
    def __init__(self):
        self.bernoulli = False
        self.actions = []  # list of strings with action names
        self.rewards = []  # list of floating points with rewards
        self.transitions = []  # list of integers with the numbers of the states that can be moved to

    def execute_action(self, actionName):
        for index in range(self.actions):
            if (actionName == self.actions[index]):
                # if bernoulli variation of the problem, return 1 or 0, depending on the reward
                if self.bernoulli:
                    randomChance = numpy.random.normal()
                    if (randomChance > self.rewards[index]):
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

class Map():
    def __init__(self):
        self.states = []

    def set_states(self, states):
        self.states = states