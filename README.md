# Genetic Algorithm for TSP (Travelling Salesman Problem)

## Project Overview
This project implements a Genetic Algorithm (GA) to solve the Travelling Salesman Problem (TSP), which involves finding the optimal path for a salesman to visit all cities exactly once and return to the starting point. The algorithm can be applied to cities or airports, visualizing the shortest path and demonstrating the power of Genetic Algorithms in combinatorial optimization problems.

## Table of Contents
- [Introduction](#introduction)
- [Genetic Algorithm Overview](#genetic-algorithm-overview)
- [Algorithm Steps](#algorithm-steps)
- [Visualization](#visualization)
- [Usage](#usage)
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
