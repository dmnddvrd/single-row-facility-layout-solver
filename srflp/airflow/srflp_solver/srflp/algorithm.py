import numpy as np
import itertools
from srflp.exception import SrflpError
from srflp.chromosome import SrflpChromosome, Population
from srflp.utils.timer import stopwatch
import sys
import random

class SrflpAlgorithm:

    ALGORITHMS = [
        'RANDOM_PERMUTATION',
        'BRUTE_FORCE'
    ]
    @staticmethod
    def solve_simple(srflp_chromosome: SrflpChromosome, N, algorithm = 'RANDOM_PERMUTATION'):
        algorithm = algorithm.upper()
        if algorithm not in SrflpAlgorithm.ALGORITHMS:
            raise SrflpError(f'Incorrect algorithm provided {algorithm}')
        print(f'Using alogirthm {algorithm}')
        if algorithm == 'RANDOM_PERMUTATION':
            return SrflpAlgorithm.random_permutations(srflp_chromosome, N)
        if algorithm == 'BRUTE_FORCE':
            return SrflpAlgorithm.brute_force(srflp_chromosome, N)

#   Best solution from 1000000 iterations took 51 steps -> [3, 4, 1, 0, 5, 2] -> 2846.0
    @staticmethod
    def random_permutations(srflp_chromosome: SrflpChromosome, MAX_ITERATIONS = 10_000):
        best_fitness_val = float('inf')
        best_sol = []
        best_sol_iteration_no = 0
        for i in range(MAX_ITERATIONS):
            fitness_val = srflp_chromosome.fitness
            solution = np.random.permutation(srflp_chromosome.n).tolist()
            srflp_chromosome.F = solution
            if fitness_val < best_fitness_val:
                best_fitness_val, best_sol, best_sol_iteration_no = fitness_val, solution, i
        print(f'RANDOM PERM: Best solution from {MAX_ITERATIONS} iterations took {best_sol_iteration_no} steps -> {best_sol} -> {best_fitness_val}')

    @staticmethod
    def brute_force(srflp_chromosome: SrflpChromosome, MAX_ITERATIONS = 10_000):
        best_fitness_val = float('inf')
        best_sol = []
        best_sol_iteration_no = 0
        i = 0
        starting_arr = srflp_chromosome.F
        for permutation in itertools.permutations(starting_arr):
            i = i+1
            fitness_val = srflp_chromosome.fitness
            srflp_chromosome.F = permutation
            if fitness_val < best_fitness_val:
                best_fitness_val, best_sol, best_sol_iteration_no = fitness_val, permutation, i
            if i == MAX_ITERATIONS:
                break
        print(f'BRUTE_FORCE: Best solution from {i} iterations took {best_sol_iteration_no} steps -> {best_sol} -> {best_fitness_val}')
        return (srflp_chromosome, i, best_sol_iteration_no, best_sol,best_fitness_val)


