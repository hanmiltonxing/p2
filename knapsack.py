# Code from mlrose officical website, with some modification with ClaudeAI
import numpy as np
import mlrose_hiive as mlrose
import matplotlib.pyplot as plt
import time

# Set random seed for reproducibility
np.random.seed(69)

# Generate random weights and values for the knapsack problem
weights = np.random.rand(260)
values = np.random.rand(260)
print("Weights: ", weights)
print("Values: ", values)
print("Max Value: ", max(values))

# Initialize lists to store results
sa_fitness = []
rhc_fitness = []
ga_fitness = []
mimic_fitness = []

sa_times = []
rhc_times = []
ga_times = []
mimic_times = []

# Define the range of problem sizes
problem_sizes = range(10, 100, 10)

# Loop through different problem sizes
for size in problem_sizes:
    fitness_fn = mlrose.Knapsack(weights[:size], values[:size], 0.7)
    problem = mlrose.DiscreteOpt(length=size, fitness_fn=fitness_fn, maximize=True, max_val=2)
    problem.set_mimic_fast_mode(True)
    initial_state = np.random.randint(2, size=size)
    
    # Simulated Annealing
    start_time = time.time()
    best_state_sa, best_fitness_sa, _ = mlrose.simulated_annealing(problem, max_attempts=10, curve=True)
    end_time = time.time()
    sa_times.append(end_time - start_time)
    sa_fitness.append(best_fitness_sa)
    
    # Random Hill Climb
    start_time = time.time()
    best_state_rhc, best_fitness_rhc, _ = mlrose.random_hill_climb(problem, restarts=5, curve=True)
    end_time = time.time()
    rhc_times.append(end_time - start_time)
    rhc_fitness.append(best_fitness_rhc)
    
    # Genetic Algorithm
    start_time = time.time()
    best_state_ga, best_fitness_ga, _ = mlrose.genetic_alg(problem, pop_size=2*size, max_attempts=10, curve=True)
    end_time = time.time()
    ga_times.append(end_time - start_time)
    ga_fitness.append(best_fitness_ga)
    
    # MIMIC
    start_time = time.time()
    best_state_mimic, best_fitness_mimic, _ = mlrose.mimic(problem, pop_size=5*size, max_attempts=20, curve=True)
    end_time = time.time()
    mimic_times.append(end_time - start_time)
    mimic_fitness.append(best_fitness_mimic)

# Convert lists to numpy arrays for plotting
sa_fitness = np.array(sa_fitness)
rhc_fitness = np.array(rhc_fitness)
ga_fitness = np.array(ga_fitness)
mimic_fitness = np.array(mimic_fitness)

sa_times = np.array(sa_times)
rhc_times = np.array(rhc_times)
ga_times = np.array(ga_times)
mimic_times = np.array(mimic_times)

# Plot fitness vs. problem size
plt.figure()
plt.plot(problem_sizes, sa_fitness, label='Simulated Annealing')
plt.plot(problem_sizes, rhc_fitness, label='Randomized Hill Climb')
plt.plot(problem_sizes, ga_fitness, label='Genetic Algorithm')
plt.plot(problem_sizes, mimic_fitness, label='MIMIC')
plt.title('Fitness vs. Problem Size (Knapsack)')
plt.xlabel('Problem Size')
plt.ylabel('Fitness')
plt.legend()
plt.savefig('knapsack_fitness.png')

# Plot computation time vs. problem size
plt.figure()
plt.plot(problem_sizes, sa_times, label='Simulated Annealing')
plt.plot(problem_sizes, rhc_times, label='Randomized Hill Climb')
plt.plot(problem_sizes, ga_times, label='Genetic Algorithm')
plt.plot(problem_sizes, mimic_times, label='MIMIC')
plt.title('Time Efficiency vs. Problem Size (Knapsack)')
plt.xlabel('Problem Size')
plt.ylabel('Computation Time (s)')
plt.legend()
plt.savefig('knapsack_computation.png')

# Plot change with respect to iterations
problem_length = 80
fitness_fn = mlrose.Knapsack(weights[:problem_length], values[:problem_length], 0.65)
problem = mlrose.KnapsackOpt(length=problem_length, fitness_fn=fitness_fn, maximize=True, max_val=2)
problem.set_mimic_fast_mode(True)
initial_state = np.zeros((problem_length,), dtype=int)

_, _, sa_curve = mlrose.simulated_annealing(problem, schedule=mlrose.ExpDecay(), max_attempts=10, curve=True)
_, _, rhc_curve = mlrose.random_hill_climb(problem, restarts=5, curve=True)
_, _, ga_curve = mlrose.genetic_alg(problem, pop_size=2*problem_length, max_attempts=10, curve=True)
_, _, mimic_curve = mlrose.mimic(problem, pop_size=5*problem_length, max_attempts=20, curve=True)

# Plot fitness curve
plt.figure()
# Plot the fitness curves for different optimization algorithms

# Plot the fitness curve for Simulated Annealing
plt.plot(
    (np.arange(1, len(sa_curve) + 1) / len(sa_curve)),  # Normalized x-axis values
    sa_curve[:, 1],  # y-axis values (fitness scores)
    label='Simulated Annealing'  # Label for the legend
)

# Plot the fitness curve for Randomized Hill Climb
plt.plot(
    (np.arange(1, len(rhc_curve) + 1) / len(rhc_curve)),  # Normalized x-axis values
    rhc_curve[:, 1],  # y-axis values (fitness scores)
    label='Randomized Hill Climb'  # Label for the legend
)

# Plot the fitness curve for Genetic Algorithm
plt.plot(
    (np.arange(1, len(ga_curve) + 1) / len(ga_curve)),  # Normalized x-axis values
    ga_curve[:, 1],  # y-axis values (fitness scores)
    label='Genetic Algorithm'  # Label for the legend
)

# Plot the fitness curve for MIMIC
plt.plot(
    (np.arange(1, len(mimic_curve) + 1) / len(mimic_curve)),  # Normalized x-axis values
    mimic_curve[:, 1],  # y-axis values (fitness scores)
    label='MIMIC'  # Label for the legend
)

# Set the title of the plot
plt.title('Fitness Curve (Knapsack)')

# Display the legend
plt.legend()

# Show the plot
plt.show()
plt.title('Fitness Curve (Knapsack)')
plt.xlabel('Percentage of Iterations')
plt.ylabel('Fitness Evaluations')
plt.legend()
plt.savefig('knapsack_fitness_eval.png')

# Plot iterations vs fitness
plt.figure()
plt.plot(sa_curve[:, 0], label='Simulated Annealing')
plt.plot(rhc_curve[:, 0], label='Randomized Hill Climb')
plt.plot(ga_curve[:, 0], label='Genetic Algorithm')
plt.plot(mimic_curve[:, 0], label='MIMIC')
plt.title('Fitness Curve (Knapsack)')
plt.xlabel('Iterations')
plt.ylabel('Fitness')
plt.legend()
plt.savefig('knapsack_iterations.png')
