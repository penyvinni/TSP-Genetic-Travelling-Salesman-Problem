import numpy as np
import random

# Step-1: Randomly create the initial population
def generate_population(num_individuals, num_cities):
    population = []
    for _ in range(num_individuals):
        chromosome = list(range(num_cities))
        random.shuffle(chromosome)
        population.append(chromosome)
    return population

# Example matrix representation of the cost of the path between two cities
# Replace this with your actual cost matrix
cost_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

# Step-2: Assign fitness to each chromosome
def calculate_fitness(chromosome, cost_matrix):
    total_cost = sum(cost_matrix[chromosome[i-1]][chromosome[i]] for i in range(len(chromosome)))
    return 1 / total_cost

# Roulette Wheel Selection
def select_parents(population, cost_matrix):
    fitness_values = [calculate_fitness(chromosome, cost_matrix) for chromosome in population]
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]

    parent_indices = np.random.choice(range(len(population)), size=len(population), p=probabilities, replace=False)
    parents = [population[i] for i in parent_indices]
    return parents

# Step-3: Create new offspring population by applying crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

# Step-4: Mutate offspring if required
def mutate(offspring, mutation_rate):
    if random.random() < mutation_rate:
        mutation_point1, mutation_point2 = random.sample(range(len(offspring)), k=2)
        offspring[mutation_point1], offspring[mutation_point2] = offspring[mutation_point2], offspring[mutation_point1]
    return offspring

# Step-5: Repeat steps 3 and 4 until an optimal solution is found
def genetic_algorithm(num_generations, population_size, mutation_rate, cost_matrix, elitism=True):
    population = generate_population(population_size, len(cost_matrix))

    for generation in range(num_generations):
        population = sorted(population, key=lambda x: calculate_fitness(x, cost_matrix), reverse=True)
        parents = select_parents(population, cost_matrix)
        offspring1, offspring2 = crossover(parents[0], parents[1])
        offspring1 = mutate(offspring1, mutation_rate)
        offspring2 = mutate(offspring2, mutation_rate)

        # Replace the least fit individuals with the new offspring
        population[-2], population[-1] = offspring1, offspring2

        if elitism:
            # Keep the best individuals from the current generation unchanged in the next generation
            # elite_size = int(population_size * 0.1)  # Adjust the elite size as needed
            elite_size = 2
            elite = population[:elite_size]
            population[:elite_size] = elite

        print(f"Generation {generation + 1}: Best Fitness = {calculate_fitness(population[0], cost_matrix)}")

    return population[0]

# Example usage
num_generations = 50
population_size = 10
mutation_rate = 0.2
optimal_solution = genetic_algorithm(num_generations, population_size, mutation_rate, cost_matrix)
print("Optimal Solution:", optimal_solution)