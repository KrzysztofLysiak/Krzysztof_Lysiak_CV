import numpy as np
import matplotlib.pyplot as plt

# Objective function
def shift_r(x):
    return np.concatenate((np.zeros_like(x[..., :, -1:]), x[..., :, :-1]), axis=-1)

def shift_l(x):
    return np.concatenate((x[..., :, 1:], np.zeros_like(x[..., :, :1])), axis=-1)

def shift_t(x):
    return np.concatenate((np.zeros_like(x[..., -1:, :]), x[..., :-1, :]), axis=-2)

def shift_b(x):
    return np.concatenate((x[..., 1:, :], np.zeros_like(x[..., :1, :])), axis=-2)

def evaluate(x, size=20):
    grid = np.reshape(x, (-1, size, size))
    points = np.minimum(shift_r(grid) + shift_l(grid) + shift_t(grid) + shift_b(grid), 1 - grid)
    return points.reshape(np.shape(x)).sum(-1)

# Initialize population
def initialize_population(pop_size, genome_length):
    return np.random.randint(0, 2, size=(pop_size, genome_length))

# Roulette wheel selection
def roulette_wheel_selection(population, fitness):
    probabilities = fitness / np.sum(fitness)
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    return population[selected_indices]

# One-point crossover
def crossover(parent1, parent2):
    point = np.random.randint(1, len(parent1))
    child1 = np.concatenate((parent1[:point], parent2[point:]))
    child2 = np.concatenate((parent2[:point], parent1[point:]))
    return child1, child2

# Mutation
def mutate(individual, mutation_rate):
    mutation_mask = np.random.rand(len(individual)) < mutation_rate
    individual[mutation_mask] = 1 - individual[mutation_mask]
    return individual

# Genetic algorithm
def genetic_algorithm(pop_size=100, genome_length=400, generations=100, crossover_rate=0.7, mutation_rate=0.01):
    population = initialize_population(pop_size, genome_length)
    best_fitness_over_time = []
    
    for generation in range(generations):
        fitness = evaluate(population)
        best_fitness_over_time.append(np.max(fitness))
        
        # Selection
        selected_population = roulette_wheel_selection(population, fitness)
        
        # Crossover
        next_population = []
        for i in range(0, pop_size, 2):
            if np.random.rand() < crossover_rate:
                child1, child2 = crossover(selected_population[i], selected_population[i+1])
            else:
                child1, child2 = selected_population[i], selected_population[i+1]
            next_population.extend([child1, child2])
        
        # Mutation
        population = np.array([mutate(ind, mutation_rate) for ind in next_population])
    
    best_solution = population[np.argmax(evaluate(population))]
    return best_solution, best_fitness_over_time

# Run the algorithm
best_solution, fitness_history = genetic_algorithm()

# Visualize the best solution
def visualize_solution(solution):
    grid = solution.reshape(20, 20)
    plt.imshow(grid, cmap='gray', interpolation='nearest')
    plt.title("Best solution")
    plt.show()

visualize_solution(best_solution)

# Visualize optimization progress
plt.plot(fitness_history)
plt.xlabel("Generation")
plt.ylabel("Best objective function value")
plt.title("Genetic algorithm progress")
plt.show()
