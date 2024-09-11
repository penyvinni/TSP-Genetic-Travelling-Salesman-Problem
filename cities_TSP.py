# Neural Networks using Genetic Algorithms
# TSP Problem for cities

import numpy as np
import random
import matplotlib.pyplot as plt  # for plotting
import networkx as nx  # for graphs

# Step-1: Randomly create the initial population
# Η συνάρτηση αυτή δημιουργεί τον αρχικό πληθυσμό. 
# Κάθε individual δλδ άτομο (χρωμόσωμα) αναπαρίσταται ως μια λίστα πόλεων που ανακατεύονται τυχαία.
def generate_population(num_individuals, num_cities):
    population = []
    for _ in range(num_individuals):
        chromosome = random.sample(range(num_cities), k=num_cities)
        population.append(chromosome)
    return population

# Example matrix representation of the cost of the path between two cities
# Replace this with your actual cost matrix
# δημιουργεί έναν τυχαίο πίνακα κόστους που αντιπροσωπεύει την απόσταση μεταξύ των πόλεων
def generate_cost_matrix(num_cities):
    return np.random.randint(1, 50, size=(num_cities, num_cities))

# Step-2: Assign fitness to each chromosome
# υπολογίζει την καταλληλότητα ενός ατόμου (χρωμοσώματος) με βάση το συνολικό κόστος της διαδρομής που αντιπροσωπεύει το συγκεκριμένο χρωμόσωμα. 
# Η καταλληλότητα (fitness) ορίζεται ως το αντίστροφο του συνολικού κόστους.
def calculate_fitness(chromosome, cost_matrix):
    total_cost = sum(cost_matrix[chromosome[i - 1]][chromosome[i]] for i in range(len(chromosome)))
    return 1 / total_cost

# Roulette Wheel Selection
# χρησιμοποιεί την επιλογή ρουλέτας για την επιλογή γονέων από τον πληθυσμό με βάση την καταλληλότητά τους. 
# Τα άτομα με υψηλότερη καταλληλότητα έχουν μεγαλύτερη πιθανότητα να επιλεγούν.
def select_parents(population, cost_matrix):
    fitness_values = [calculate_fitness(chromosome, cost_matrix) for chromosome in population]
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]

    parent_indices = np.random.choice(range(len(population)), size=len(population), p=probabilities, replace=False)
    parents = [population[i] for i in parent_indices]
    return parents

# Step-3: Create new offspring population by applying crossover
# εκτελεί διασταύρωση μεταξύ δύο γονέων. 
# Επιλέγει τυχαία ένα σημείο διασταύρωσης και δημιουργεί δύο παιδιά συνδυάζοντας τμήματα των γονέων.
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

# Step-4: Mutate offspring if required
# mutation_rate = ποσοστο μεταλλαξης
# εισάγει μετάλλαξη στους απογόνους με ορισμένη πιθανότητα. 
# Ανταλλάσσει τις θέσεις δύο τυχαία επιλεγμένων γονιδίων (genes).
def mutate(offspring, mutation_rate):
    if random.random() < mutation_rate:
        mutation_point1, mutation_point2 = random.sample(range(len(offspring)), k=2)
        offspring[mutation_point1], offspring[mutation_point2] = offspring[mutation_point2], offspring[mutation_point1]
        print(f"Mutation: Swapped genes at positions {mutation_point1} and {mutation_point2} in offspring {offspring}")

    return offspring

    
# Visualization of the best path
def plot_path(cost_matrix, optimal_solution, all_connections=False):
    num_cities = len(optimal_solution)
    plt.figure()

    if optimal_solution is not None:
        # Create a directional graph for the optimal solution
        G = nx.DiGraph()
        for i in range(num_cities - 1):
            G.add_edge(optimal_solution[i], optimal_solution[i + 1])
        G.add_edge(optimal_solution[-1], optimal_solution[0])

        # Draw the graph on the existing plot with directional nodes, arrows, markers, and labels
        pos = {i: (cost_matrix[i][0], cost_matrix[i][1]) for i in optimal_solution}
        nx.draw_networkx(G, pos, with_labels=True, node_size=300, font_size=8, node_color='red', font_color='white', font_weight='bold', connectionstyle='arc3,rad=0.1', arrowsize=15, arrowstyle='->')

    if all_connections:
        # Draw all connections between cities in finer lines
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                plt.plot([cost_matrix[i][0], cost_matrix[j][0]], [cost_matrix[i][1], cost_matrix[j][1]], linestyle=':', color='gray', alpha=0.5)

    # Add a caption with distances
    distances_caption = "\n".join([f"City {i} to City {j}: {cost_matrix[i][j]}" for i in range(num_cities) for j in range(num_cities) if i != j])
    plt.figtext(0.85, 0.02, f'Distances:\n{distances_caption}', ha='left', va='bottom', fontsize=8, color='blue')

    plt.suptitle(f'Optimal Solution: {optimal_solution}')
    plt.show()

    
# Display distances between cities
def display_distances(cost_matrix):
    num_cities = len(cost_matrix)
    print("Distances between cities:")
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                print(f"City {i} to City {j}: {cost_matrix[i][j]}")
                
# plot the convergence of the best fitness over generations to demonstrate how the algorithm improves over time. 
# def plot_convergence(generation_costs):
#     plt.figure()
#     generations = range(1, len(generation_costs) + 1)
#     plt.plot(generations, generation_costs, marker='o', linestyle='-', color='b')
#     plt.title('Convergence of Total Cost over Generations')
#     plt.xlabel('Generation')
#     plt.ylabel('Total Cost')
#     plt.grid()
#     plt.show()

# Step-5: Repeat steps 3 and 4 until an optimal solution is found
# Η κύρια συνάρτηση genetic_algorithm επαναλαμβάνει έναν καθορισμένο αριθμό γενεών. 
# Επιλέγει τους γονείς, εκτελεί διασταύρωση και μετάλλαξη και αντικαθιστά τα λιγότερο κατάλληλα άτομα με τους νέους απογόνους. 
# Εάν είναι ενεργοποιημένο το elitism, διατηρεί τα καλύτερα άτομα σε κάθε γενιά.
def genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, num_cities, elitism=True):
    cost_matrix = generate_cost_matrix(num_cities)
    population = generate_population(population_size, num_cities)

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
# Το παράδειγμα χρήσης αρχικοποιεί τον γενετικό αλγόριθμο με συγκεκριμένες παραμέτρους και εκτυπώνει τη βέλτιστη λύση που βρέθηκε. 
# Ο χρήστης καλείται να εισάγει τον αριθμό των πόλεων.
num_cities = int(input("Enter the number of cities: "))  # Get user input for the number of cities
population_size = int(input("Enter the population size: "))
num_generations = int(input("Enter the number of generations: "))
mutation_rate = float(input("Enter the mutation rate: "))
crossover_rate = float(input("Enter the crossover rate: "))
cost_matrix = generate_cost_matrix(num_cities)

# Display distances before running the algorithm
display_distances(cost_matrix)

# After running the genetic algorithm
optimal_solution = genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, num_cities)

# Display distances after running the algorithm
# display_distances(cost_matrix)  # Uncomment if needed

print("\n--------------------------------------------------------------------------------\n")
print("Optimal Solution:", optimal_solution)
print("\n--------------------------------------------------------------------------------\n")

# Prompt for user interaction
user_choice = input("Do you want to visualize the optimal solution? (yes/no): ").lower()

if user_choice == 'yes':
    # Display the graph with the optimal solution and all connections before the optimal solution is found
    plot_path(cost_matrix, optimal_solution, all_connections=True)


# Ο αλγόριθμος στοχεύει στην εύρεση μιας βέλτιστης λύσης, η οποία αντιπροσωπεύεται από το χρωμόσωμα με την υψηλότερη καταλληλότητα (χαμηλότερο συνολικό κόστος). 
# Η διαδικασία εξέλιξης περιλαμβάνει την επιλογή γονέων, την εφαρμογή διασταύρωσης και μετάλλαξης και την ενημέρωση του πληθυσμού σε αρκετές γενιές. 
# Η πρόοδος του αλγορίθμου εκτυπώνεται σε κάθε γενιά, δείχνοντας την καλύτερη καταλληλότητα που επιτυγχάνεται.

'''
cost_matrix [[25 39 41 48  6]
 [23 40 27  6 27]
 [ 7 13 38 46 46]
 [ 1 39 16 46 28]
 [49 38 11 31 12]]
 '''