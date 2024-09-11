# Genetic Algorithm for TSP (Travelling Salesman Problem)

## Project Overview
This project implements a Genetic Algorithm (GA) to solve the Travelling Salesman Problem (TSP), which involves finding the optimal path for a salesman to visit all cities exactly once and return to the starting point. The algorithm can be applied to cities or airports, visualizing the shortest path and demonstrating the power of Genetic Algorithms in combinatorial optimization problems.

## Table of Contents
- [Introduction](#introduction)
- [Genetic Algorithm Overview](#genetic-algorithm-overview)
- [Algorithm Steps](#algorithm-steps)
- [Visualization](#visualization)
- [Conclusions](#conclusions)

## Introduction
The Travelling Salesman Problem (TSP) is a classical combinatorial optimization problem where the goal is to find the shortest possible route that visits a given set of cities once and returns to the origin. The Genetic Algorithm (GA) is a heuristic search method that mimics the process of natural selection to find optimal or near-optimal solutions to such problems.

This implementation demonstrates the use of GAs to solve the TSP by representing potential solutions as chromosomes, selecting parents based on fitness, and applying crossover and mutation operations to evolve the population over generations.

## Genetic Algorithm Overview
The Genetic Algorithm used in this project follows these core steps:
1. **Generate Initial Population**: Randomly generate a set of chromosomes, where each chromosome represents a possible tour of cities.
2. **Fitness Evaluation**: Calculate the fitness of each chromosome based on the total cost (distance) of the path it represents.
3. **Selection**: Use a roulette wheel selection mechanism to select the best-fit parents for the next generation.
4. **Crossover**: Create new offspring by performing crossover between two parent chromosomes.
5. **Mutation**: Introduce random mutations with a defined mutation rate to maintain diversity in the population.
6. **Elitism**: Optionally keep the best individuals from each generation to ensure that the best solution is preserved.

## Algorithm Steps
1. **Generate Population**: 
   The initial population consists of randomly shuffled cities (chromosomes).
   ```python
   def generate_population(num_individuals, num_cities):
       # Returns a list of chromosomes
   
2. **Fitness Calculation**: 
   The fitness of each chromosome is the inverse of the total path cost.
   ```python
   def calculate_fitness(chromosome, cost_matrix):
       # Returns the fitness value of a chromosome

3. **Selection**: 
   Select parents based on their fitness using roulette wheel selection.
   ```python
   def select_parents(population, cost_matrix):
       # Returns a list of selected parents

4. **Crossover and Mutation**: 
   Perform crossover between parents and apply mutations to the offspring.
   ```python
   def crossover(parent1, parent2):
      # Returns two offspring after crossover

   def mutate(offspring, mutation_rate):
      # Mutates offspring based on the mutation rate

5. **Main Genetic Algorithm**:
   The process is repeated for a fixed number of generations.
   ```python
   def genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, num_cities, elitism=True):
       # Executes the genetic algorithm


## Visualization
The project includes a visualization function to display the optimal solution found by the Genetic Algorithm. The cities are represented as nodes, and the optimal path is visualized as directed edges.
    ```python
    def plot_path(cost_matrix, optimal_solution, all_connections=False):
       # Visualizes the optimal solution on a graph



## Conclusions
This project demonstrates how Genetic Algorithms can effectively solve the Travelling Salesman Problem. By simulating the process of natural evolution, GAs can find near-optimal solutions in a reasonable amount of time. Further improvements can be made by tweaking the parameters such as population size, mutation rate, crossover strategy, and the use of elitism.

This solution can be adapted for different optimization problems, such as airport routing, logistics, or any other pathfinding scenario.
