import run_algorithm
import matplotlib.pyplot as plt
import numpy as np

def plot_array(array, iterations):
    average_y = []
    window = 100
    for ind in range(len(array) - window + 1):
        average_y.append(np.mean(array[ind:ind+window]))
    for ind in range(window - 1):
        average_y.insert(0, np.nan)
    plt.plot(range(0, iterations), average_y)
    plt.show()

if __name__ == '__main__':
    iterations = 50000
    runs = 0
    queen_array = np.zeros(iterations)
    # rook_array = np.fromfile('temp.txt', dtype = float, count = -1,  sep = '\n')
    for i in range(runs):
        queen_array += run_algorithm.run_algorithm(True, 'queen', 8, 10, iterations)
        np.savetxt("temp.txt", queen_array, delimiter=' ', newline='\n')
        print("Finished set " + str(i + 1) + " of " + str(runs))

    #np.savetxt("SARSA_50", queen_array, delimiter=' ', newline='\n')
    #plot_array(queen_array, iterations)
    plot_array(queen_array, iterations)

