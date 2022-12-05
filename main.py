import algorithms

if __name__ == "__main__":
    N, actionCount = 1000, 5
    for bernoulli in range(0, 1):           # run the gaussian and bernoulli version of the problem
        greedyAverage, greedyCorrect = 0
        for experiment in range(0, 1000):
            BanditProblem = algorithms.make_bandit(actionCount, bernoulli)
            average, correct = algorithms.run_algorithm(BanditProblem, N, "greedy")
            greedyAverage += average
            greedyCorrect += correct


        if bernoulli:
            print("Average reward and correct percentage for greedy in the bernoulli problem:")
        else:
            print("Average reward and correct percentage for greedy in the gaussian problem:")
        greedyAverage /= float(1000)                       # average reward obtained in a run of the algorithm
        greedyCorrect /= float(1000)                       # average amount of times the algorithm selects the best option
