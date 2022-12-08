import numpy as np
import objects
import random
import matplotlib.pyplot as plt


def plot_graph(listOfLists, accuracyList, title="Trend of rewards during learning"):
    label_set = ["egreedy_gaussian", "egreedy_bernoulli", "greedy_gaussian", "greedy_bernoulli", "optimistic_gauss",
                 "optimistic_bernoulli", "ucb_gaussian", "ucb_bernoulli", "action_pref_gauss", "action_pref_bernoulli"]
    N = len(listOfLists[0])
    plt.figure(figsize=(12, 8))
    for index in range(len(listOfLists)):
        plt.plot(listOfLists[index], label=label_set[index])
    plt.legend()
    plt.title(title)
    plt.ylabel("Average reward")
    plt.xlabel("Time step")
    print("Average proportion of optimal answers per algorithm: ")
    for index in range(len(accuracyList)):
        print(label_set[index] + ": " + str(accuracyList[index]))
    plt.show()


def run_algorithm(bandit, N, algoName, ucb, optimistic, preferences):
    totalRewardAction = np.zeros(len(bandit.get_actions()))  # the amount of reward for each action
    totalActionInstances = np.zeros(len(bandit.get_actions()))  # amount of times each action has been selected
    averageExpectedReward = np.zeros(len(bandit.get_actions()))  # average reward per action, initialized to 0
    probabilities = np.zeros(len(bandit.get_actions()))
    if optimistic:
        averageExpectedReward = np.ones(len(bandit.get_actions()))  # average reward per action, initialized to 1

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
            averageExpectedReward, probabilities = update_preferences(action, probabilities, averageExpectedReward,
                                                                      reward, totalReward/(iteration+1))
        # implementation of upper confidence-bound
        elif ucb:
            averageExpectedReward = u_c_b(averageExpectedReward, totalRewardAction, totalActionInstances, iteration)
        else:
            averageExpectedReward[action] = float(totalRewardAction[action]) / float(totalActionInstances[action])

    # the amount of correct answers is the index of the answer with the highest reward's frequency
    best_answer = bandit.get_current_best_action()
    totalCorrect = totalActionInstances[best_answer]
    # return the total reward, and the total no. of optimal choices
    if totalReward >= 1000:
        print(averageExpectedReward)
    return totalReward / float(N), totalCorrect / float(N), rewardList


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
        average_expected_reward[i] = float(total_action_reward[i]) / (float(total_action_instances[i]) + 1) \
                                     + calculate_uncertainty(total_action_instances[i] + 1, t + 1)

    return average_expected_reward


def calculate_uncertainty(n, t):
    c = 0.4  # value with which we tamper for better performance
    return c * np.sqrt(np.log(t) / n)


def update_preferences(chosen_action_idx, probabilities, preferences, reward, average_reward):
    alpha = 2.75

    probabilities[chosen_action_idx] = boltzmann_distribution(chosen_action_idx, preferences)
    preferences[chosen_action_idx] = preferences[chosen_action_idx] + alpha * (reward - average_reward) \
                                     * (1 - probabilities[chosen_action_idx])
    for i in range(len(preferences)):
        if i != chosen_action_idx:
            probabilities[i] = boltzmann_distribution(i, preferences)
            preferences[i] = preferences[i] - alpha * (reward - average_reward) * probabilities[i]

    return preferences, probabilities


def boltzmann_distribution(idx, preferences):
    s = 0
    for x in preferences:
        s += np.exp(x)
    return np.exp(preferences[idx]) / s


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
