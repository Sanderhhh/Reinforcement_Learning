import numpy as np
import objects
import random


def run_algorithm(bandit, N, algoName):
    totalReward, totalCorrect = 0, 0
    actions = bandit.getActions
    total_reward_action = np.zeros(length(bandit.getActions()))          # the amount of reward for each action
    total_action_instances = np.zeros(length(bandit.getActions()))       # amount of times each action has been selected
    average_expected_reward = np.ones(length(bandit.getActions()))       # average reward per action, initialized to 1
    for iteration in range(0, N):
        pass
    return totalReward, totalCorrect  # return the total reward, and the total no. of optimal choices

def algo_chooser(algoName, average_expected_reward):
    if (algoName == "greedy"):
        return greedy(average_expected_reward)
    elif ():
        pass



def greedy(average_expected_reward):
    return np.argmax(average_expected_reward)


def e_greedy(actions, estimates, epsilon):
    num = random.random()
    if num < epsilon:
        return random.choice(actions)
    else:
        return greedy(actions, estimates)


def optimistic_initial_values(length):
    optimistic_estimates = []
    for i in range(length):
        optimistic_estimates.append(random.randrange(70, 100))

    return optimistic_estimates


def ucb(actions, estimates, action_counters, t):
    ucb_estimates = []
    for i in range(len(actions)):
        ucb_estimates.append(estimates[i] + calculate_uncertainty(action_counters[i], t))

    return greedy(actions, ucb_estimates)


def calculate_uncertainty(n, t):
    c = 1.5  # value with which we tamper for better performance
    return c * np.sqrt(np.log(t) / n)


def action_preferences():
    return


def make_bandit(actionCount, bernoulli):
    Bandit = objects.Map()
    state = objects.State()
    # set actions with rewards appropriate to the normal (gaussian) distribution
    for action in range(0, actionCount):
        state.set_action(action, np.random.normal(), 0)

    # Set if it is the bernoulli version of the problem
    if bernoulli:
        state.bernoulli = True
    Bandit.set_states(state)
    return Bandit
