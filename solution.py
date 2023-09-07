import numpy as np
import pandas as pd
import random
import csv

#Loading Distance Matrix
distance_matrix = pd.read_csv("Distance_Matrix.csv", index_col=0).values
#Loading biomass froecast data from fromat.csv
biomass_forecast = pd.read_csv('forecast2.csv').set_index('Index')['2018'].to_dict()

#Problem-specific paramenters
LOCATIONS = 2418
REFINERIES = 4
DEPOTS = 20
DEPOT_CAP = 20000
REFINERY_CAP = 100000


#Genetic algorithm Parameters
population_size = 140
num_genrations = 60
mutation_rate =0.1

#Create initial population:
def create_chromosome():
    refinery_indices = np.random.choice(LOCATIONS, REFINERIES, replace= False)
    depot_indices =  np.random.choice(LOCATIONS, DEPOTS, replace= False)
    return np.concatenate((refinery_indices, depot_indices))

#{Objective function}: Assigning biomass to depot
def assign_biomass_to_depot(biomass_data, depots, distance_matrix):
    biomass_to_process = (sum(biomass_data.values())*0.8)
    biomass_processed = 0
    # print("Biomass to process: ",biomass_to_process)
    heap = []
    for loc in biomass_data:
        for depot_id, depot_index in enumerate(depots):
            distance = distance_matrix[loc, depot_index]
            heap.append((distance, loc, depot_id,depots[depot_id]))
    heap = sorted(heap)
    
    assignment = [None]*len(biomass_data)
    depot_load = [0]*len(depots)
    biomass_processed = 0
    for i in heap:
        distance,loc,depot_id, depot = i[0],i[1],i[2],i[3]
        if assignment[loc] is None:
            depot_load[depot_id]+=biomass_data[loc]
            if depot_load[depot_id]< DEPOT_CAP:
                assignment[loc] = depot
            else:
                depot_load[depot_id]-=biomass_data[loc] 
    return assignment,depot_load


# {Objective function}: Assigning refinery to depot
def assign_refinery_to_depot(biomass_load, refineries, distance_matrix):
    heap = []
    # print(f"biomass_load: {biomass_load}, refineries: {refineries}")
    for depot_loc in range(len(biomass_load)):
        for refinery_id, refinery_index in enumerate(refineries):
            distance = distance_matrix[depot_loc, refinery_index]
            heap.append((distance, depot_loc, refinery_id, refineries[refinery_id]))
    heap = sorted(heap)

    assignment = [None]*len(biomass_load)
    refinery_load = [0]*len(refineries)
     
    for i in heap:
        distance,depot_loc,refinery_id, refinery = i[0],i[1],i[2],i[3]
        if assignment[depot_loc]==None:
            refinery_load[refinery_id]+=biomass_load[depot_loc]
            if refinery_load[refinery_id]>= REFINERY_CAP:
                refinery_load[refinery_id]-=biomass_load[depot_loc]
                continue
            else:
                assignment[depot_loc] = refinery
    # print("refinery assignment: ",assignment)
    return assignment,refinery_load

#Evaluating chromosomes:
def evaluate_chromosome(chromosome):
    refinery_indices = chromosome[:REFINERIES]
    depot_indices = chromosome[REFINERIES:]

    #Getting depots and refinery locations, loads from functions:
    depot_assignments, depot_load = assign_biomass_to_depot(biomass_forecast, depot_indices, distance_matrix)
    refinery_assignments, refinery_load = assign_refinery_to_depot(depot_load,refinery_indices,distance_matrix)

    cost_of_transportation = 0
    for i in range(len(depot_assignments)):
        if depot_assignments[i]==None:
            continue
        else:
            cost_of_transportation += (distance_matrix[i,depot_assignments[i]]*biomass_forecast[i]) #node and depot assigned for node
    for i in range(len(refinery_assignments)):
        if refinery_assignments[i]==None:
            continue
        else:
            cost_of_transportation+= (distance_matrix[i,refinery_assignments[i]]*depot_load[i])
    total_depot_cap = 420000
    total_depot_load = sum(depot_load)

    total_refinery_cap = 400000
    total_refinery_load = sum(refinery_load)

    cost_of_underutilization = (total_depot_cap-total_depot_load)+(total_refinery_cap-total_refinery_load)
    cost = ((cost_of_transportation*0.001)+cost_of_underutilization) 
    fitness = (100-((80*cost)/500000)) #It is the score
    return fitness

population = [create_chromosome() for _ in range(population_size)] #Getting population
max_fitness=0
iteration=0
#Main Genetic Algotithm loop
for generation in range(num_genrations):
    fitness_values = [evaluate_chromosome(chromosome) for chromosome in population]

    selected_indices = np.random.choice(len(population), size=population_size , replace=False, p=np.array(fitness_values) / np.sum(fitness_values))
    offspring = []
    
    for i in range(0, len(selected_indices) - 1, 2):
        parent1 = population[selected_indices[i]]
        parent2 = population[selected_indices[i + 1]]
        crossover_point = np.random.randint(1, len(parent1) - 1)
        child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        offspring.extend([child1, child2])

        for j in range(len(offspring)):
            if np.random.rand() < mutation_rate:
                mutation_point = np.random.randint(len(offspring[j]))
                offspring[j][mutation_point] = np.random.randint(LOCATIONS)
        
    population = offspring
    if fitness_values[np.argmax(fitness_values)]> max_fitness:
        max_fitness = fitness_values[np.argmax(fitness_values)]
        max_solution = population[np.argmax(fitness_values)]
    print(f"Max fitness value for this iteration is: {max_fitness}")
    print("iteration: ",iteration)
    iteration+=1
    print("looping...")

#Find the best solution
best_solution_index = np.argmax(fitness_values)
best_solution = population[best_solution_index]
best_fitness = fitness_values[best_solution_index]

print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
print(best_solution_index)
print(len(population))
print()
print("max solution: ",max_solution)
print("max fitness: ", max_fitness)

# is_output = input("Do you want the csv output of this result?(y/n): ")
# if is_output=="y":
#     csv_output(max_solution)
