import json
import numpy as np
import itertools
from srflp.exception import SrflpError
from srflp.data.generator import SrflpTableGenerator

class SrflpTable:

    MIN_N = 2
    MAX_N = 100

    def __str__(self):
        return json.dumps({
            'n': self.n,
            'F': self.F,
            'L': self.L,
            'C': self.C,
        })

    def __init__(self, n, L, C):
        if n < 2 or n > self.MAX_N:
            raise SrflpError(f'Incorrect input for table provided (n={n} should be between {self.MIN_N} and {self.MAX_N})')
        if not L or not C:
            raise SrflpError('Empty dataset provided')
        if len(L) != n or len(C) != n or [x for x in C if len(x) != n] != []:
            raise SrflpError(f'Incorrect dimensions provided: {type(self)} : {self}')
        for i in range(n):
            if C[i][i] != -1:
                raise SrflpError(f'Incorrect cost matrix provided {self}')
        for i in range(n):
            for j in range(n):
                if i != j and C[i][j] < 0:
                    raise SrflpError(f'Inccorect cost matrix provided {self}')
        self.n = n
        self.F = [x for x in range(n)]
        self.L = L
        self.C = C 

class SrflpAlgorithm:

    ALGORITHMS = [
        'RANDOM_PERMUTATION',
        'BRUTE_FORCE'
    ]
    
    @staticmethod
    def get_distance(srflp_table: SrflpTable, i, j)->float:
        sum = 0
        if i > j:
            i,j = j,i
        for k in srflp_table.F[i+1:j]:
            sum = sum + srflp_table.L[k]
        distance = (srflp_table.L[i] + srflp_table.L[j]) / 2 + sum
        return distance

    @staticmethod
    def get_fitness(srflp_table: SrflpTable)->float:
        sum = 0
        for i in range(srflp_table.n-1):
            for j in range(i+1, srflp_table.n):
                if i != j:
                    sum = sum + srflp_table.C[i][j] * SrflpAlgorithm.get_distance(srflp_table, i, j)
        return sum 

    @staticmethod
    def solve(srflp_table: SrflpTable, N, algorithm = 'RANDOM_PERMUTATION'):
        algorithm = algorithm.upper()
        if algorithm not in SrflpAlgorithm.ALGORITHMS:
            raise SrflpError(f'Incorrect algorithm provided {algorithm}')
        if algorithm == 'RANDOM_PERMUTATION':
            SrflpAlgorithm.random_permutations(srflp_table, N)
        if algorithm == 'BRUTE_FORCE':
            SrflpAlgorithm.brute_force(srflp_table, N)


#   Best solution from 1000000 iterations took 51 steps -> [3, 4, 1, 0, 5, 2] -> 2846.0
    @staticmethod
    def random_permutations(srflp_table: SrflpTable, MAX_ITERATIONS = 10**5):
        best_fitness_val = 99999
        best_sol = []
        best_sol_iteration_no = 0
        for i in range(MAX_ITERATIONS):
            fitness_val = SrflpAlgorithm.get_fitness(srflp_table)
            solution = np.random.permutation(srflp_table.n).tolist()
            srflp_table.F = solution
            if fitness_val < best_fitness_val:
                best_fitness_val = fitness_val
                best_sol = solution
                best_sol_iteration_no = i
        print(f'RANDOM PERM: Best solution from {MAX_ITERATIONS} iterations took {best_sol_iteration_no} steps -> {best_sol} -> {best_fitness_val}')

    @staticmethod
    def brute_force(srflp_table: SrflpTable, MAX_ITERATIONS = 10**5):
        best_fitness_val = 99999
        best_sol = []
        best_sol_iteration_no = 0
        i = 0
        starting_arr = srflp_table.F
        for permutation in itertools.permutations(starting_arr):
            i = i+1
            fitness_val = SrflpAlgorithm.get_fitness(srflp_table)
            srflp_table.F = permutation
            if fitness_val < best_fitness_val:
                best_fitness_val = fitness_val
                best_sol = permutation
                best_sol_iteration_no = i
        print(f'BRUTE_FORCE: Best solution from {i} iterations took {best_sol_iteration_no} steps -> {best_sol} -> {best_fitness_val}')

# def main():
#     N = 10**6
#     n = 6
#     L = [20, 10, 16, 20, 10, 10]
#     C = [
#             [-1, 12, 3, 6, 0, 20],
#             [12, -1, 5, 5, 5, 0],
#             [3, 5, -1, 10, 4, 2],
#             [6, 5, 10, -1, 2, 12],
#             [0, 5, 4, 2, -1, 6],
#             [20, 0, 2, 12, 6, -1]
#         ]
#     x = SrflpTable(n,L,C)
#     SrflpAlgorithm.solve(x, N, 'brute_force')
    
def main():
    for n in range(49,50):
        for table in SrflpTableGenerator.generate_sample(19):
            SrflpAlgorithm.solve(table, 100, 'brute_force')
            SrflpAlgorithm.solve(table, 100, 'RANDOM_PERMUTATION')
        
if __name__ == "__main__":
    main()