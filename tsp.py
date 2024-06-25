# From https://mlrose.readthedocs.io/en/stable/source/tutorial2.html
import numpy as np 
import mlrose_hiive
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import preprocessing, datasets
import time
import random
import warnings

np.random.seed(50)

dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426), \
             (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000), \
             (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426), \
             (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721), \
             (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056), \
             (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623), \
             (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]

coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]

coords_list = [(0, 1), (0, 2), (0, 4), (1, 3), (2, 0), (2, 3), (3, 4),(1, 2), (2, 4), (1, 5), (1, 6), (1, 4), (3, 4), (4, 5), (2, 3), (2, 4), (2, 6), (3, 5), (4, 2), (4, 5), (5, 6), (7, 6), (2, 7), (4, 1), (4, 1)]

fitness_simulated_annealing = []
fitness_random_hill_climb = []
fitness_genetic_algorithm = []
fitness_mimic = []

time_simulated_annealing = []
time_random_hill_climb = []
time_genetic_algorithm = []
time_mimic = []


problem_length = 20
fitness = mlrose_hiive.TravellingSales(coords = coords_list[:problem_length])
problem = mlrose_hiive.TSPOpt(length = problem_length, fitness_fn = fitness, maximize = False)
problem.set_mimic_fast_mode(True)
init_state = np.random.choice(problem_length, size = problem_length, replace = False)
_, _, fitness_curve_sa = mlrose_hiive.simulated_annealing(problem, init_state = init_state, curve = True)
print("Done with SA iterations!")
_, _, fitness_curve_rhc = mlrose_hiive.random_hill_climb(problem, init_state = init_state, curve = True)
print("Done with RHC iterations!")
_, _, fitness_curve_ga = mlrose_hiive.genetic_alg(problem, curve = True)
print("Done with GA iterations!")
_, _, fitness_curve_mimic = mlrose_hiive.mimic(problem, pop_size = 1000, curve = True)
print("Done with MIMIC iterations!")

plt.figure()
plt.plot(fitness_curve_sa[:,0], label = 'Simulated Annealing')
plt.plot(fitness_curve_rhc[:,0], label = 'Randomized Hill Climb')
plt.plot(fitness_curve_ga[:,0], label = 'Genetic Algorithm')
plt.plot(fitness_curve_mimic[:,0], label = 'MIMIC')
plt.title('Fitness Curve (TSP)')
plt.legend()
plt.xlabel('Iterations')
plt.ylabel('Fitness')
plt.savefig('tsp_iterations.png')


import numpy as np
import mlrose_hiive
import matplotlib.pyplot as plt
import time

np.random.seed(50)

# List of problem sizes to test
problem_sizes = [5, 10, 15, 20]

# Initialize lists to store results
fitness_simulated_annealing = []
fitness_random_hill_climb = []
fitness_genetic_algorithm = []
fitness_mimic = []

time_simulated_annealing = []
time_random_hill_climb = []
time_genetic_algorithm = []
time_mimic = []

function_evals_sa = []
function_evals_rhc = []
function_evals_ga = []
function_evals_mimic = []

coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3),
               (2, 4), (1, 5), (1, 6), (1, 4), (3, 4), (4, 5), (2, 3), (2, 4),
               (2, 6), (3, 5), (4, 2), (4, 5), (5, 6), (7, 6), (2, 7), (4, 1), (4, 1)]

for problem_length in problem_sizes:
    fitness = mlrose_hiive.TravellingSales(coords=coords_list[:problem_length])
    problem = mlrose_hiive.TSPOpt(length=problem_length, fitness_fn=fitness, maximize=False)
    problem.set_mimic_fast_mode(True)
    
    init_state = np.random.choice(problem_length, size=problem_length, replace=False)
    
    # Simulated Annealing
    start_time = time.time()
    _, best_fitness_sa, fitness_curve_sa = mlrose_hiive.simulated_annealing(problem, init_state=init_state, curve=True)
    end_time = time.time()
    fitness_simulated_annealing.append(best_fitness_sa)
    time_simulated_annealing.append(end_time - start_time)
    function_evals_sa.append(len(fitness_curve_sa))
    
    # Randomized Hill Climbing
    start_time = time.time()
    _, best_fitness_rhc, fitness_curve_rhc = mlrose_hiive.random_hill_climb(problem, init_state=init_state, curve=True)
    end_time = time.time()
    fitness_random_hill_climb.append(best_fitness_rhc)
    time_random_hill_climb.append(end_time - start_time)
    function_evals_rhc.append(len(fitness_curve_rhc))
    
    # Genetic Algorithm
    start_time = time.time()
    _, best_fitness_ga, fitness_curve_ga = mlrose_hiive.genetic_alg(problem, curve=True)
    end_time = time.time()
    fitness_genetic_algorithm.append(best_fitness_ga)
    time_genetic_algorithm.append(end_time - start_time)
    function_evals_ga.append(len(fitness_curve_ga))
    
    # MIMIC
    start_time = time.time()
    _, best_fitness_mimic, fitness_curve_mimic = mlrose_hiive.mimic(problem, pop_size=1000, curve=True)
    end_time = time.time()
    fitness_mimic.append(best_fitness_mimic)
    time_mimic.append(end_time - start_time)
    function_evals_mimic.append(len(fitness_curve_mimic))

# Plotting Fitness Curves for Different Problem Sizes
plt.figure(figsize=(12, 8))
plt.plot(problem_sizes, fitness_simulated_annealing, label='Simulated Annealing')
plt.plot(problem_sizes, fitness_random_hill_climb, label='Randomized Hill Climb')
plt.plot(problem_sizes, fitness_genetic_algorithm, label='Genetic Algorithm')
plt.plot(problem_sizes, fitness_mimic, label='MIMIC')
plt.title('Best Fitness vs. Problem Size (TSP)')
plt.legend()
plt.xlabel('Problem Size')
plt.ylabel('Best Fitness')
plt.savefig('fitness_vs_problem_size.png')

# Plotting Computation Time for Different Problem Sizes
plt.figure(figsize=(12, 8))
plt.plot(problem_sizes, time_simulated_annealing, label='Simulated Annealing')
plt.plot(problem_sizes, time_random_hill_climb, label='Randomized Hill Climb')
plt.plot(problem_sizes, time_genetic_algorithm, label='Genetic Algorithm')
plt.plot(problem_sizes, time_mimic, label='MIMIC')
plt.title('Computation Time vs. Problem Size (TSP)')
plt.legend()
plt.xlabel('Problem Size')
plt.ylabel('Computation Time (s)')
plt.savefig('time_vs_problem_size.png')

# Plotting Function Evaluations for Different Problem Sizes
plt.figure(figsize=(12, 8))
plt.plot(problem_sizes, function_evals_sa, label='Simulated Annealing')
plt.plot(problem_sizes, function_evals_rhc, label='Randomized Hill Climb')
plt.plot(problem_sizes, function_evals_ga, label='Genetic Algorithm')
plt.plot(problem_sizes, function_evals_mimic, label='MIMIC')
plt.title('Function Evaluations vs. Problem Size (TSP)')
plt.legend()
plt.xlabel('Problem Size')
plt.ylabel('Function Evaluations')
plt.savefig('function_evals_vs_problem_size.png')

plt.show()
