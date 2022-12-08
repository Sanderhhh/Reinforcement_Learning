import algorithms

if __name__ == "__main__":
    N, actionCount, experimentCount = 1000, 50, 500
    optimistic, ucb, preferences = 0, 0, 0
    print("Experiments run with " + str(N) + " iterations, " +
          str(actionCount) + " actions and " + str(experimentCount) + " experiments per setup.")
    rewardsPerAlgo = []
    accuracyList = []
    for algo in range(5):
        if algo == 0:                  # set the algorithm that we want to use
            algorithm = "e_greedy"
        elif algo == 1:
            algorithm = "greedy"
        elif algo == 2:
            optimistic = 1
        elif algo == 3:
            optimistic = 0
            ucb = 1
        elif algo == 4:
            ucb = 0
            preferences = 1

        for bernoulli in range(0, 2):  # run the gaussian and bernoulli version of the problem
            greedyAverage, greedyCorrect = 0, 0
            rewardList = [0] * N
            for experiment in range(0, experimentCount):
                BanditProblem = algorithms.make_bandit(actionCount, bernoulli)
                average, correct, experimentList = algorithms.run_algorithm(BanditProblem, N, algorithm, ucb, optimistic, preferences)
                for index in range(len(experimentList)):
                    rewardList[index] += experimentList[index]
                greedyAverage += average
                greedyCorrect += correct

            if bernoulli:
                print("Average reward and correct percentage for " + algorithm + " in the bernoulli problem:")
            else:
                print("Average reward and correct percentage for " + algorithm + " in the gaussian problem:")
            if ucb:
                print("Using ucb")
            if optimistic:
                print("Using optimistic initial values")
            if preferences:
                print("Using action preferences")
            greedyAverage /= float(experimentCount)  # average reward obtained in a run of the algorithm
            greedyCorrect /= float(experimentCount)  # average amount of times the algorithm selects the best option
            print("Average reward: " + str(greedyAverage))
            print("Proportion of correct answers: " + str(greedyCorrect))

            print()

            for index in range(len(rewardList)):
                rewardList[index] /= experimentCount
            rewardsPerAlgo.append(rewardList)

            accuracyList.append(greedyCorrect)

    # plot the things
    algorithms.plot_graph(rewardsPerAlgo, accuracyList)
