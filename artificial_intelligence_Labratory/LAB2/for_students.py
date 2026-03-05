from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *


def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness

def wyborRodzicow(items, knapsack_max_capacity, population, n_selection):
    fitSum = sum(fitness(items, knapsack_max_capacity, osobnik) for osobnik in population)
    fitOs = [fitness(items, knapsack_max_capacity, osobnik)/fitSum for osobnik in population]
    parents = random.choices(population, weights=fitOs, k=n_selection)
    return parents, fitOs

def tworzenieKolejnegoPokolenia(parents, population_size, n_elite):
    new_generation = []
    for _ in range(population_size - n_elite):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        crossover_point = random.randint(0, len(items))
        child = parent1[:crossover_point] + parent2[crossover_point:]
        new_generation.append(child)
    return new_generation

def mutacja(new_generation):
    for child in new_generation:
        random_gene = random.randint(0, len(child) - 1)
        child[random_gene] = not child[random_gene]


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 20
n_elite = 1

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
for _ in range(generations):
    population_history.append(population)

    # TODO: implement genetic algorithm
    #2.1.2
    parents, weights = wyborRodzicow(items, knapsack_max_capacity, population, n_selection)
    #2.1.3
    new_generation = tworzenieKolejnegoPokolenia(parents, population_size, n_elite)
    #najlepszy, _ = population_best(items, knapsack_max_capacity, population)
    #new_generation.append(najlepszy)

    #2.1.4
    mutacja(new_generation)
    #2.1.5
    selected= random.choices(population, k=population_size-len(new_generation), weights=weights)
    population = new_generation + selected

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
