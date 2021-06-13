import json
from srflp.exception import SrflpError
import srflp.utils.config as config
import numpy as np
import random 

# Permutational representation of a Chromosome
# Ex: For n = 4 can be [0,1,2,3], [0,3,2,1], etc.
class Chromosome:
    MIN_N = 3
    MAX_N = 100

    def __init__(self, n, F = None):
        if n < self.MIN_N or n > self.MAX_N:
            raise SrflpError(f'Incorrect input provided for chromosome (n={n} should be between {self.MIN_N} and {self.MAX_N})')
        self._F = [x for x in range(n)] if not F else F
        
class SrflpChromosome(Chromosome):

    def __init__(self, n, L, C, F=None):
        super().__init__(n)
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
        self.__F = [x for x in range(n)] if not F else F
        self.L = L
        self.C = C 
        self.fitness = self.get_fitness()

    def order_crossover(self, chr_b:Chromosome):
        a,b = self.F[:], chr_b.F[:]
        offspring = [None]*self.n
        offset = self.n // 2
        start = random.randint(0, self.n-offset)
        stop = start + offset
        offspring[start:stop] = a[start:stop]
        b_ind, c_ind  = stop, stop
        l = self.n
        while None in offspring:
            if b[b_ind % l] not in offspring:
                offspring[c_ind % l] = b[b_ind % l]
                c_ind += 1
            b_ind += 1
        return SrflpChromosome(self.n, self.L, self.C, offspring)

    def partially_mapped_crossover(self, other: Chromosome):
        a,b = self.F[:], other.F[:]
        offspring = [None]*self.n
        offset = self.n // 2
        start = random.randint(0, self.n-offset)
        stop = start + offset
        # Copy a slice from first parent:
        offspring[start:stop] = a[start:stop]
        # Map the same slice in parent b to child using indices from parent a:
        for ind,x in enumerate(b[start:stop]):
            ind += start
            if x not in offspring:
                while offspring[ind] != None:
                    ind = b.index(a[ind])
                offspring[ind] = x
        # Copy over the rest from parent b
        for ind,x in enumerate(offspring):
            if x == None:
                offspring[ind] = b[ind]
        return SrflpChromosome(self.n, self.L, self.C, offspring)

    @property
    def F(self):
        return self.__F
    
    @F.setter
    def F(self, F):
        if len(F) != len(self.__F):
            raise SrflpError(f'New F value should be same length as original')
        self.__F = F
        self.fitness = self.get_fitness() 

    # Returns distance between `i`th and `j`th facilities
    def get_distance(self, i, j)->float:
        if i == j:
            return 0
        if i > j:
            i,j = j,i
        sum = 0
        for k in self.__F[i+1:j]:
            sum += self.L[k]
        distance = (self.L[i] + self.L[j]) / 2 + sum
        return distance

    # Swaps 2 facilities at random of the given chromosome nr_of_swaps times
    # [0, 1, 3, 5, 4, 2], we pick [2, 5] as a,b and thus the array becomes [0, 1, 2, 5, 4, 3]
    def swap_mutation(self, nr_of_swaps=1):
        for _i in range(nr_of_swaps):
            a,b = random.randint(0, self.n-1),random.randint(0, self.n-1)
            while b==a:
                b = random.randint(0, self.n-1)
            self.F[a], self.F[b] = self.F[b], self.F[a]
            self.fitness = self.get_fitness()

    # Picks two indices in a chromosome a,b <n ; a<b
    # Shifts the element from index b to be the next to a and the rest of the elements remain the same  
    # [0, 1, 3, 5, 4, 2], we pick [2, 5] as a,b and thus the array becomes [0, 1, 3, 2, 5, 4]
    def insert_mutation(self):
        a,b = random.randint(0, self.n-1),random.randint(0, self.n-1)
        while b==a:
            b = random.randint(0, self.n-1)
        if a>b:
            a,b =b,a
        self.F.insert(a+1, self.F[b])
        del self.F[b+1]
        self.fitness = self.get_fitness()

    # Picks a subset from an array and rearranges it randomly
    def scramble_mutation(self):
        a,b = random.randint(0, self.n-1),random.randint(0, self.n-1)
        while abs(b-a)<2:
            b = random.randint(0, self.n-1)
        if a>b:
            a,b =b,a
        temp = self.F[a:b]
        random.shuffle(temp)
        self.F[a:b] = temp
        self.fitness = self.get_fitness()

    # Picks a subset from an array and rearranges it randomly
    def reverse_mutation(self):
        a,b = random.randint(0, self.n-1),random.randint(0, self.n-1)
        while abs(b-a)<2:
            b = random.randint(0, self.n-1)
        if a>b:
            a,b =b,a
        temp = self.F[a:b]
        temp.reverse()
        self.F[a:b] = temp
        self.fitness = self.get_fitness()

    def mutation(self, type: str):
        type = type.lower()
        if type == 'reverse':
            self.reverse_mutation()
        elif type == 'scramble':
            self.scramble_mutation()
        elif type == 'insert':
            self.insert_mutation()
        elif type == 'swap':
            self.swap_mutation()
        else:
            raise SrflpError(f'Incorrect mutation {type}')

    def crossover(self, other: Chromosome, type: str):
        type = type.lower()
        if type == 'pmx':
            return self.partially_mapped_crossover(other)
        elif type == 'order':
            return self.order_crossover(other)
        else:
            raise SrflpError(f'Incorrect crossover{type}')

    # Calculates fitness of the given chromosome
    def get_fitness(self)->float:
        sum = 0
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                if i != j:
                    sum += self.C[i][j] * self.get_distance(i, j)
        return sum
        
    def __str__(self):
        return json.dumps({
            'n': self.n,
            'F': self.__F,
            'L': self.L,
            'C': self.C,
        })

class Population():
    DEFAULT_POP_SIZE = config.get('default_pop_size')

    def __init__(self, population=None):
        if population and not all(isinstance(x, Chromosome) for x in population):
            raise SrflpError(f'All members of a population must be Chromosomes')
        self.population = population if population else []
        self.n = len(population) if population else 0
    
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
        def wraper(function):
            def wrapped_f(*args, **kwargs):
                print(f'Applied {operation_type} operation ({function.__name__}) to population')
                return function(*args,**kwargs)
            return wrapped_f
        return wraper

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
    def selection_roulette_wheel(self, selection_size):
        n = len(self.population)
        if selection_size > n:
            raise SrflpError(f'Cannot create bigger sample({selection_size}) than the original population ({n})')
        return Population(random.choices(self.population, weights=[x.fitness for x in self.population], k=selection_size))
    
    # Rank selection finds the N best chromosomes of a given population based on fitness
    def selection_rank(self, selection_size):
        n = len(self.population)
        if selection_size > n:
            raise SrflpError(f'Cannot create bigger sample({selection_size}) than the original population ({n})')
        indices = np.argsort([x.fitness for x in self.population])[-selection_size:].tolist() 
        pop = []
        for i in indices:
            pop.append(self.population[i])
        return Population(pop)

    # Completely random selection
    def selection_rand(self, selection_size):
        n = len(self.population)
        if selection_size > n:
            raise SrflpError(f'Cannot create bigger sample({selection_size}) than the original population ({n})')
        return Population(random.choices(self.population, k=selection_size))

    def __str__(self):
        return '\n'.join([str(x.F) for x in self.population])