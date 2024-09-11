import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import cartopy.crs as ccrs

# Step-1: Randomly create the initial population
def generate_population(num_individuals, num_airports, time_windows):
    population = []
    for _ in range(num_individuals):
        chromosome = random.sample(range(num_airports), k=num_airports)
        population.append((chromosome, time_windows.copy()))
    return population

# Example matrix representation of the cost of the path between two airports
# Replace this with your actual cost matrix
def generate_cost_matrix(num_airports):
    return np.random.randint(1, 50, size=(num_airports, num_airports))

# Step-2: Assign fitness to each chromosome
def calculate_fitness(chromosome, cost_matrix):
    total_cost = sum(cost_matrix[chromosome[0][i - 1]][chromosome[0][i]] for i in range(len(chromosome[0])))
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
    crossover_point = random.randint(1, len(parent1[0]) - 1)
    child1 = (parent1[0][:crossover_point] + [gene for gene in parent2[0] if gene not in parent1[0][:crossover_point]], parent1[1].copy())
    child2 = (parent2[0][:crossover_point] + [gene for gene in parent1[0] if gene not in parent2[0][:crossover_point]], parent2[1].copy())
    return child1, child2

# Step-4: Mutate offspring if required
def mutate(offspring, mutation_rate):
    if random.random() < mutation_rate:
        mutation_point1, mutation_point2 = random.sample(range(len(offspring[0])), k=2)
        offspring[0][mutation_point1], offspring[0][mutation_point2] = offspring[0][mutation_point2], offspring[0][mutation_point1]
        print(f"Mutation: Swapped genes at positions {mutation_point1} and {mutation_point2} in offspring {offspring[0]}")

    return offspring

# Visualization of the best path    
def plot_path_on_map(cost_matrix, optimal_solution):
    num_airports = len(optimal_solution[0])
    
    # Create a map using Cartopy
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([min(cost_matrix[:, 0]) - 5, max(cost_matrix[:, 0]) + 5, min(cost_matrix[:, 1]) - 5, max(cost_matrix[:, 1]) + 5])
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    
    optimal_x = [cost_matrix[optimal_solution[0][i]][0] for i in range(num_airports)]
    optimal_y = [cost_matrix[optimal_solution[0][i]][1] for i in range(num_airports)]

    plt.plot(optimal_x, optimal_y, marker='s', markersize=8, linestyle='dashed', label='Optimal Solution', color='red')

    for airport in range(num_airports):
        plt.text(cost_matrix[airport][0], cost_matrix[airport][1], str(airport), fontsize=12, color='blue')

    plt.title(f'Optimal Solution:{optimal_solution[0]}')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.show()


# Display distances between airports
def display_distances(cost_matrix):
    num_airports = len(cost_matrix)
    print("Distances between airports:")
    for i in range(num_airports):
        for j in range(num_airports):
            if i != j:
                print(f"Airport {i} to Airport {j}: {cost_matrix[i][j]}")

# Step-5: Repeat steps 3 and 4 until an optimal solution is found
def genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, num_airports, time_windows, elitism=True):
    cost_matrix = generate_cost_matrix(num_airports)
    population = generate_population(population_size, num_airports, time_windows)

    for generation in range(num_generations):
        population = sorted(population, key=lambda x: calculate_fitness(x, cost_matrix), reverse=True)
        parents = select_parents(population, cost_matrix)
        print(f"\nGeneration {generation + 1}")
        print(f"Parents: {parents}")
        offspring1, offspring2 = crossover(parents[0], parents[1])

        # Apply mutation after crossover
        offspring1 = mutate(offspring1, mutation_rate)
        offspring2 = mutate(offspring2, mutation_rate)

        # Replace the least fit individuals with the new offspring
        population[-2], population[-1] = offspring1, offspring2

        if elitism:
            # Keep the best individuals from the current generation unchanged in the next generation
            elite_size = int(population_size * 0.1)  # Adjust the elite size as needed
            elite = population[:elite_size]
            population[:elite_size] = elite

        best_fitness = calculate_fitness(population[0], cost_matrix)
        print(f"Best Fitness = {best_fitness}")
        print(f"Best Path: {population[0]}")
        print("\n\n")

    return population[0]

# Example usage
num_airports = int(input("Enter the number of airports: "))
population_size = int(input("Enter the population size: "))
num_generations = int(input("Enter the number of generations: "))
mutation_rate = 0.2
crossover_rate = 0.8
time_windows = [(0, 100), (50, 150), (30, 120), (80, 200)]  # Replace with your time window constraints

# Generate cost matrix
cost_matrix = generate_cost_matrix(num_airports)

# Display distances before running the algorithm
display_distances(cost_matrix)

# After running the genetic algorithm
optimal_solution = genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, num_airports, time_windows)

# Display distances after running the algorithm
display_distances(cost_matrix)

# optimal_solution[0] και οχι optimal_solution γιατι ειναι tuple με path και time_windows
print("\n--------------------------------------------------------------------------------\n")
print("Optimal Solution (Path):", optimal_solution[0])
print("\n--------------------------------------------------------------------------------\n")


# Display the map with the optimal solution highlighted
plot_path_on_map(cost_matrix, optimal_solution)