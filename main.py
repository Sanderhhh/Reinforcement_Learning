import algorithms

if __name__ == "__main__":
    N, actionCount, experimentCount = 1000, 50, 1000
    for algo in range(0, 2):
        if algo == 0:                  # set the algorithm that we want to use
            algorithm = "greedy"
        else:
            algorithm = "e_greedy"

        for bernoulli in range(0, 2):  # run the gaussian and bernoulli version of the problem
            greedyAverage, greedyCorrect = 0, 0
            for experiment in range(0, experimentCount):
                BanditProblem = algorithms.make_bandit(actionCount, bernoulli)
                average, correct = algorithms.run_algorithm(BanditProblem, N, algorithm)
                greedyAverage += average
                greedyCorrect += correct

            if bernoulli:
                print("Average reward and correct percentage for " + algorithm + " in the bernoulli problem:")
            else:
                print("Average reward and correct percentage for " + algorithm + " in the gaussian problem:")
            greedyAverage /= float(experimentCount)  # average reward obtained in a run of the algorithm
            greedyCorrect /= float(experimentCount)  # average amount of times the algorithm selects the best option
            print("Average reward: " + str(greedyAverage))
            print("Proportion of correct answers: " + str(greedyCorrect))
