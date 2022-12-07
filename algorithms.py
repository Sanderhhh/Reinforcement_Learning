import matplotlib
import numpy as np
import objects
import random
import matplotlib.pyplot as plt


def plot_graph(listOfLists, title = "new2"):
    label_set = ["egreedy_gaussian", "egreedy_bernoulli", "greedy_gaussian", "greedy_bernoulli", "optimistic_gauss",
                 "optimistic_bernoulli", "ucb_gaussian", "ucb_bernoulli", "action_pref_gauss", "action_pref_bernoulli"]
    N = len(listOfLists[0])
    zeros = [0] * N
    for index in range(len(listOfLists)):
        plt.plot(listOfLists[index], label = label_set[index])
    plt.legend(label_set)
    plt.title(title)
    plt.ylabel("Average reward")
    plt.xlabel("Iteration")
    plt.show()


def run_algorithm(bandit, N, algoName, ucb, optimistic, preferences):
    totalRewardAction = np.zeros(len(bandit.get_actions()))      # the amount of reward for each action
    totalActionInstances = np.zeros(len(bandit.get_actions()))   # amount of times each action has been selected
    averageExpectedReward = np.zeros(len(bandit.get_actions()))  # average reward per action, initialized to 0
    probabilities = np.zeros(len(bandit.get_actions()))
    if optimistic:
        averageExpectedReward = np.ones(len(bandit.get_actions()))  # average reward per action, initialized to 1
    previous_action = -1

    totalReward = 0
    rewardList = []
    for iteration in range(0, N):
        # select an action according to the algorithm
        if preferences:
            if iteration == 0:
                action = random.choice(list(range(0, len(probabilities))))
            else:
                action = random.choices(list(range(0, len(probabilities))), weights=probabilities, k=1)[0]
        else:
            action = algo_chooser(algoName, averageExpectedReward)
        reward = bandit.execute_actions(action)
        totalReward += reward
        rewardList.append(totalReward / float(iteration + 1))
        # update the total reward for the action, the amount of action instances, and the average expected reward for it
        totalRewardAction[action] += float(reward)
        totalActionInstances[action] += 1
        # implementation of action preferences
        if preferences:
            averageExpectedReward = update_preferences(previous_action, action,
                                                       averageExpectedReward, 1/float(totalActionInstances[action]),
                                                       reward, averageExpectedReward[action])
            probabilities = update_probabilities(averageExpectedReward, probabilities)
        # implementation of upper confidence-bound
        elif ucb:
            averageExpectedReward = u_c_b(averageExpectedReward, totalRewardAction, totalActionInstances, iteration)
        else:
            averageExpectedReward[action] = float(totalRewardAction[action]) / float(totalActionInstances[action])
        previous_action = action

    # the amount of correct answers is the index of the answer with the highest reward's frequency
    best_answer = bandit.get_current_best_action()
    totalCorrect = totalActionInstances[best_answer]
    # return the total reward, and the total no. of optimal choices
    if totalReward >= 1000:
        print(averageExpectedReward)
    return totalReward / float(N), totalCorrect / float(N), rewardList


def update_probabilities(preferences, probabilities):
    for i in range(len(preferences)):
        probabilities[i] = boltzmann_distribution(i, preferences)

    return probabilities


def algo_chooser(algoName, average_expected_reward):
    if algoName == "greedy":
        return greedy(average_expected_reward)
    elif algoName == "e_greedy":
        return e_greedy(average_expected_reward)


def greedy(average_expected_reward):
    return np.argmax(average_expected_reward)


def e_greedy(average_expected_reward, epsilon=0.1):
    num = random.uniform(0, 1)
    if num < epsilon:
        return random.randint(0, len(average_expected_reward) - 1)
    else:
        return np.argmax(average_expected_reward)


def u_c_b(average_expected_reward, total_action_reward, total_action_instances, t):
    for i in range(len(average_expected_reward)):
        if total_action_instances[i] == 0:
            average_expected_reward[i] = calculate_uncertainty(total_action_instances[i], t + 1)
        else:
            average_expected_reward[i] = float(total_action_reward[i]) / float(total_action_instances[i]) \
                                    + calculate_uncertainty(total_action_instances[i], t + 1)

    return average_expected_reward


def calculate_uncertainty(n, t):
    c = 5.5  # value with wich we tamper for better performance
    if n == 0:
        return c * np.sqrt(np.log(t))
    return c * np.sqrt(np.log(t) / n)


def update_preferences(previous_action_idx, chosen_action_idx, preferences, alpha, reward, average_reward):
    policy = boltzmann_distribution(chosen_action_idx, preferences)
    preferences[chosen_action_idx] = preferences[chosen_action_idx] + alpha * (reward - average_reward) * (1 - policy)
    if previous_action_idx != chosen_action_idx and previous_action_idx != -1:
        preferences[previous_action_idx] = preferences[chosen_action_idx] + alpha * (reward - average_reward) * policy

    return preferences


def boltzmann_distribution(idx, preferences):
    sum = 0
    for x in preferences:
        sum += np.exp(x)
    return np.exp(preferences[idx]) / sum


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
