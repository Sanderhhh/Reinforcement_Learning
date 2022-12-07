import numpy as np
import objects
import random


def run_algorithm(bandit, N, algoName):
    totalRewardAction = np.zeros(len(bandit.get_actions()))  # the amount of reward for each action
    totalActionInstances = np.zeros(len(bandit.get_actions()))  # amount of times each action has been selected
    averageExpectedReward = np.ones(len(bandit.get_actions()))  # average reward per action, initialized to 1
    action_preferences = np.ones(len(bandit.get_actions())) # action preferences per action, initialized to 1
    for iteration in range(0, N):
        action = algo_chooser(algoName, averageExpectedReward)  # select an action according to the algorithm
        reward = bandit.execute_actions(action)
        # update the total reward for the action, the amount of action instances, and the average expected reward for it
        totalRewardAction[action] += reward
        totalActionInstances[action] += 1
        averageExpectedReward[action] = float(totalRewardAction[action]) / float(totalActionInstances[action])

    # calculate the total reward
    totalReward = 0
    for reward in totalRewardAction:
        totalReward += reward

    # the amount of correct answers is the index of the answer with the highest reward's frequency
    best_answer = bandit.get_current_best_action()
    totalCorrect = totalActionInstances[best_answer]
    # return the total reward, and the total no. of optimal choices
    if totalReward >= 1000:
        print(averageExpectedReward)
    return totalReward / float(N), totalCorrect / float(N)


def algo_chooser(algoName, average_expected_reward):
    if algoName == "greedy":
        return greedy(average_expected_reward)
    elif algoName == "e_greedy":
        return e_greedy(average_expected_reward)
    elif algoName == "optimistic":
        return optimistic_initial_values(len(average_expected_reward))
    elif algoName == "ucb":
        return


def greedy(average_expected_reward):
    return np.argmax(average_expected_reward)


def e_greedy(average_expected_reward, epsilon=0.1):
    num = random.uniform(0, 1)
    if num < epsilon:
        return random.randint(0, len(average_expected_reward) - 1)
    else:
        return np.argmax(average_expected_reward)


def optimistic_initial_values(length):
    optimistic_estimates = []
    for i in range(length):
        optimistic_estimates.append(random.randrange(70, 100))

    return optimistic_estimates


def ucb(actions, estimates, action_counters, t):
    ucb_estimates = []
    for i in range(len(actions)):
        ucb_estimates.append(estimates[i] + calculate_uncertainty(action_counters[i], t))
    return greedy(actions)


def calculate_uncertainty(n, t):
    c = 1.5  # value with which we tamper for better performance
    return c * np.sqrt(np.log(t) / n)


def action_preferences():
    return


def update_preferences(previous_action_idx, chosen_action_idx, preferences, alpha, reward, average_reward):
    policy = boltzmann_distribution(chosen_action_idx, preferences)
    preferences[chosen_action_idx] = preferences[chosen_action_idx] + alpha * (reward - average_reward) * (1 - policy)
    if previous_action_idx != chosen_action_idx:
        preferences[previous_action_idx] = preferences[chosen_action_idx] + alpha * (reward - average_reward) * policy

    return preferences


def boltzmann_distribution(idx, preferences):
    return np.exp(preferences[idx]) / np.sum(preferences)


def make_bandit(actionCount, bernoulli):
    Bandit = objects.Map()
    state = objects.State()
    # set actions with rewards appropriate to the normal (gaussian) distribution
    for action in range(0, actionCount):
        state.set_action(action, random.uniform(0, 1), 0)

    # Set if it is the bernoulli version of the problem
    if bernoulli:
        state.bernoulli = True
    Bandit.set_states(state)
    return Bandit
