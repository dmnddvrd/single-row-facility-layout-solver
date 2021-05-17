import numpy as np
import itertools
from srflp.exception import SrflpError
from srflp.table import SrflpTable
from srflp.utils.timer import stopwatch
import sys

class SrflpAlgorithm:

    ALGORITHMS = [
        'RANDOM_PERMUTATION',
        'BRUTE_FORCE'
    ]
    DEFAULT_POPUPATION_SIZE = 10

    @staticmethod
    def solve_simple(srflp_table: SrflpTable, N, algorithm = 'RANDOM_PERMUTATION'):
        algorithm = algorithm.upper()
        if algorithm not in SrflpAlgorithm.ALGORITHMS:
            raise SrflpError(f'Incorrect algorithm provided {algorithm}')
        print(f'Using alogirthm {algorithm}')
        if algorithm == 'RANDOM_PERMUTATION':
            SrflpAlgorithm.random_permutations(srflp_table, N)
        if algorithm == 'BRUTE_FORCE':
            SrflpAlgorithm.brute_force(srflp_table, N)


#   Best solution from 1000000 iterations took 51 steps -> [3, 4, 1, 0, 5, 2] -> 2846.0
    @staticmethod
    @stopwatch
    def random_permutations(srflp_table: SrflpTable, MAX_ITERATIONS = 10**5):
        best_fitness_val = float('inf')
        best_sol = []
        best_sol_iteration_no = 0
        for i in range(MAX_ITERATIONS):
            fitness_val = srflp_table.get_fitness()
            solution = np.random.permutation(srflp_table.n).tolist()
            srflp_table.F = solution
            if fitness_val < best_fitness_val:
                best_fitness_val, best_sol, best_sol_iteration_no = fitness_val, solution, i
        print(f'RANDOM PERM: Best solution from {MAX_ITERATIONS} iterations took {best_sol_iteration_no} steps -> {best_sol} -> {best_fitness_val}')

    @staticmethod
    @stopwatch
    def brute_force(srflp_table: SrflpTable, MAX_ITERATIONS = 10**5):
        best_fitness_val = float('inf')
        best_sol = []
        best_sol_iteration_no = 0
        i = 0
        starting_arr = srflp_table.F
        for permutation in itertools.permutations(starting_arr):
            i = i+1
            fitness_val = srflp_table.get_fitness()
            srflp_table.F = permutation
            if fitness_val < best_fitness_val:
                best_fitness_val, best_sol, best_sol_iteration_no = fitness_val, permutation, i
            if i == MAX_ITERATIONS:
                break
        print(f'BRUTE_FORCE: Best solution from {i} iterations took {best_sol_iteration_no} steps -> {best_sol} -> {best_fitness_val}')


    @staticmethod
    def genetic_algorithm(srflp_table: SrflpTable,popupation_size=10,selection_type=None, crossover_type=None, mutation_type=None):
        pass
