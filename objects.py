class state():
    def __init__(self):
        self.actions = []       # list of strings with action names
        self.rewards = []       # list of integers with rewards
        self.transitions = []   # list of integers with the numbers of the states that can be moved to

    def execute_action(self, actionName):
        for index in range(self.actions):
            if (actionName == self.actions[index]):
                return self.rewards[index], self.transitions[index]
        return 0, 0             # return statement if the action name is invalid

    def set_action(self, actionName, actionReward, actionTransition):
        # set the names and values of the actions
        self.actions.append(actionName)
        self.rewards.append(actionReward)
        self.transitions.append(actionTransition)

    def get_actions(self):
        return self.actions     # return the list of action names

class map():
    def __init__(self):
        self.states = []
