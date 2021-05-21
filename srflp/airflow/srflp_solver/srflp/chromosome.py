import json
from srflp.exception import SrflpError
import srflp.utils.config as config
from srflp.data.generator import SrflpChromosomeGenerator as srflp_gen
import numpy as np
import random 

# Permutational representation of a Chromosome
# Ex: For n = 4 can be [0,1,2,3], [0,3,2,1], etc.
class Chromosome:

    MIN_N = config.get('min_n_chromosome')
    MAX_N = config.get('max_n_chromosome')

    def __init__(self, n, F = None):
        if n < 2 or n > self.MAX_N:
            raise SrflpError(f'Incorrect input provided for chromosome (n={n} should be between {self.MIN_N} and {self.MAX_N})')
        self.F = [x for x in range(n)] if not F else F

class SrflpChromosome(Chromosome):

    def __init__(self, n, L, C, F=None):
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
        self.F = [x for x in range(n)] if not F else F
        self.L = L
        self.C = C 

    # Returns distance between `i`th and `j`th facilities
    def get_distance(self, i, j)->float:
        sum = 0
        if i == j:
            return sum
        if i > j:
            i,j = j,i
        for k in self.F[i+1:j]:
            sum = sum + self.L[k]
        distance = (self.L[i] + self.L[j]) / 2 + sum
        return distance

    # Calculates fitness of the given chromosome
    def get_fitness(self)->float:
        sum = 0
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                if i != j:
                    sum = sum + self.C[i][j] * self.get_distance(i, j)
        return sum 

        
    def __str__(self):
        return json.dumps({
            'n': self.n,
            'F': self.F,
            'L': self.L,
            'C': self.C,
        })

class Population():
    DEFAULT_POP_SIZE = config.get('default_pop_size')

    def __init__(self, population):
        if not all(isinstance(x, Chromosome) for x in population):
            raise SrflpError(f'All members of a population must be Chromosomes')
        self.population = population
        self.n = len(population)
    
    # Adds a chromosome to the population
    def add(self, chr: Chromosome):
        self.population.append(chr)

    # Removes chromosome from given index
    def remove(self, index):
        n = len(self.population)
        if index < n:
            raise SrflpError(f'Invalid index({index}) in array of length {n}')
        del self.population[index]

    # A decorator to log/print whenever a genetic operation is performed
    def genetic_operation(operation_type):
        def wrap(function):
            def wrapped_f(*args, **kwargs):
                print(f'Applied {operation_type} operation ({function.__name__}) to population')
                return function(*args,**kwargs)
            return wrapped_f
        return wrap

    # Random variable x      Index in the Cumulative Array      Value in Original Array
    # -----------------      -----------------------------      ----------------------
    #  0 <= x < 10                      0                            10
    # 10 <= x < 70                      1                            60
    # 70 <= x < 75                      2                             5
    # 75 <= x < 100                     3                            25 
    # x is 72, bisecting the cumulative array gives a position index of 2 which corresponds to 5 in the original array
    def bisection(self, arr, val):
        for i in range(len(arr)):
            if val<arr[i]:
                return i
                
    # The probability of choosing an individual for breeding of the next generation is proportional to its fitness, 
    # the better the fitness is, the higher chance for that individual to be chosen
    @genetic_operation('selection')
    def selection_roulette_wheel(self, selection_size):
        n = len(self.population)
        if selection_size > n:
            raise SrflpError(f'Cannot create bigger sample({selection_size}) than the original population ({n})')
        cummulative_fitness = np.cumsum([chromosome.get_fitness() for chromosome in self.population]) 
               
        return self.bisection(cummulative_fitness, random.random()*cummulative_fitness[-1])

    

