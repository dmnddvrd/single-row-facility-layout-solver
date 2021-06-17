from srflp.data.generator import SrflpChromosomeGenerator
from srflp.algorithm import SrflpAlgorithm
from srflp.chromosome import SrflpChromosome, Chromosome, Population
import csv, os, time 
from datetime import date
import pandas as pd
import json, random
import numpy as np

def genetic_algorithm(chr: SrflpChromosome, population_size, mutation_type, crossover_type, p_c, p_m, generations = 100):
    nr_of_crossovers = int(population_size * p_c)
    # Creating an initial population:
    generation = Population()
    # Generating initial random pop.
    for i in range(population_size):
        generation.add(SrflpChromosome(chr.n, chr.L[:], [row[:] for row in chr.C], np.random.permutation(chr.n).tolist()))
    for i in range(generations):
        generation.population = sorted(generation.population, key = lambda x:x.fitness)
        # Crossover: parents from the top 50% of the population is mating
        for i in range(nr_of_crossovers):
            parent1 = random.choice(generation.population[:int(population_size/2)])
            parent2 = random.choice(generation.population[:int(population_size/2)])
            generation.add(parent1.crossover(parent2, crossover_type))
            generation.add(parent2.crossover(parent1, crossover_type))
        # Mutation: Each individual has a p_m chance to mutate
        for chr in generation.population:
            if random.uniform(0, 1) < p_m:
                chr.mutation(mutation_type)
        # generation.population = sorted(generation.population, key = lambda x:x.fitness)
        generation.population = random.choices(generation.population, weights=[x.fitness for x in generation.population], k=population_size)
    return generation.population[-1].fitness
        
def solve_genetic():
    df = pd.read_csv('data\solutions\solutions_2021-06-12.csv')
    statistical_data = []
    header = ['i', 'n','generations', 'population_size', 'mutation_type','p_m','crossover_type','p_c','fitness_val','abs_fitness_val','execution_time', 'execution_time_brute_force', 'err', 'err_percentage', 'exec_time_rate']
    filename = f'data/solutions/solutions_GA.csv'
    with open(os.path.abspath(filename), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)    
    for i, row in df.iterrows():
        chr_json = json.loads(row['sol_chrom_json'])
        abs_fitness_val = float(row["fitness_val"])
        brute_force_exec_time = float(row["execution_time"])
        n = chr_json['n']
        x = SrflpChromosome(n, chr_json['L'], chr_json['C'])  
        for pop_size in [75]:
            # for mt_type in ['swap', 'insert', 'scramble', 'reverse']:
            for mt_type in ['insert']:
                # for crossover_type in ['pmx', 'order']:
                for crossover_type in ['pmx']:
                    for p_crossover in [0.8]:
                        for p_mutation in [0.05]:
                            for _x in range(10):
                                start_time = time.time()
                                fitness_val = genetic_algorithm(x, population_size=pop_size,mutation_type=mt_type,
                                    crossover_type=crossover_type, p_c=p_crossover, p_m=p_mutation, generations = 1000)
                                time_delta = float(time.time() - start_time)
                                time_delta_str = str(time_delta)[:6]
                                err = fitness_val - abs_fitness_val
                                err_percentage = (fitness_val * 100) / abs_fitness_val - 100
                                statistical_data.append([
                                    i, n, 500, pop_size, mt_type, p_mutation, crossover_type, p_crossover, fitness_val, abs_fitness_val, time_delta_str, brute_force_exec_time, err, err_percentage, brute_force_exec_time/time_delta 
                                ])
            print(pop_size)
        print(i)
        with open(os.path.abspath(filename), 'a') as f:
            writer = csv.writer(f)
            writer.writerows(statistical_data)
        statistical_data = []

if __name__ == "__main__":
    solve_genetic()

