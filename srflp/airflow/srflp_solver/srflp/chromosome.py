import json
from srflp.exception import SrflpError
import srflp.utils.config as config
from srflp.data.generator import SrflpChromosomeGenerator as srflp_gen
import numpy as np
import random 

# Permutational representation of a Chromosome
# Ex: For n = 4 can be [0,1,2,3], [0,3,2,1], etc.
class Chromosome:
    MIN_N = int(config.get('min_n_chromosome'))
    MAX_N = int(config.get('max_n_chromosome'))

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
    @genetic_operation('selection')
    def selection_roulette_wheel(self, selection_size):
        n = len(self.population)
        if selection_size > n:
            raise SrflpError(f'Cannot create bigger sample({selection_size}) than the original population ({n})')
        return Population(random.choices(self.population, weights=[x.fitness for x in self.population], k=selection_size))
    
    # Rank selection finds the N best chromosomes of a given population based on fitness
    @genetic_operation('selection')
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
    @genetic_operation('selection')
    def selection_rand(self, selection_size):
        n = len(self.population)
        if selection_size > n:
            raise SrflpError(f'Cannot create bigger sample({selection_size}) than the original population ({n})')
        return Population(random.choices(self.population, k=selection_size))

    # Mutate all elements specified in ch_indices array
    @genetic_operation('mutation')
    def swap_mutation(self, ch_indices, nr_of_swaps=1):
        n = len(self.population)
        if not ch_indices or not all( i < n for i in ch_indices):
            raise SrflpError(f'Indices of genes are empty or exceed upper limit {ch_indices}')
        # Doesn't matter which chromosome's N we extract since in a population all of them should be of the same dimension
        for i in ch_indices:
            self.population[i].swap_mutation(nr_of_swaps)

    @genetic_operation('mutation')
    def insert_mutation(self, ch_indices):
        n = len(self.population)
        if not ch_indices or not all( i < n for i in ch_indices):
            raise SrflpError(f'Indices of genes are empty or exceed upper limit {ch_indices}')
        # Doesn't matter which chromosome's N we extract since in a population all of them should be of the same dimension
        for i in ch_indices:
            self.population[i].insert_mutation()

    @genetic_operation('mutation')
    def scramble_mutation(self, ch_indices):
        n = len(self.population)
        if not ch_indices or not all( i < n for i in ch_indices):
            raise SrflpError(f'Indices of genes are empty or exceed upper limit {ch_indices}')
        # Doesn't matter which chromosome's N we extract since in a population all of them should be of the same dimension
        for i in ch_indices:
            self.population[i].scramble_mutation()

    @genetic_operation('mutation')
    def reverse_mutation(self, ch_indices):
        n = len(self.population)
        if not ch_indices or not all( i < n for i in ch_indices):
            raise SrflpError(f'Indices of genes are empty or exceed upper limit {ch_indices}')
        # Doesn't matter which chromosome's N we extract since in a population all of them should be of the same dimension
        for i in ch_indices:
            self.population[i].reverse_mutation()
 
    def pmx(self,chr_a: Chromosome,chr_b: Chromosome, start:int, stop:int):
        a,b = chr_a.F[:], chr_b.F[:]
        child = [None]*chr_a.n
        # Copy a slice from first parent:
        child[start:stop] = a[start:stop]
        # Map the same slice in parent b to child using indices from parent a:
        for ind,x in enumerate(b[start:stop]):
            ind += start
            if x not in child:
                while child[ind] != None:
                    ind = b.index(a[ind])
                child[ind] = x
            # Copy over the rest from parent b
        for ind,x in enumerate(child):
            if x == None:
                child[ind] = b[ind]
        return child


    def ox(self, chr_a: Chromosome, chr_b:Chromosome, start:int, stop:int):
        a,b = chr_a.F[:], chr_b.F[:]
        child = [None]*chr_a.n
        child[start:stop] = a[start:stop]
        b_ind, c_ind  = stop, stop
        l = chr_a.n
        while None in child:
            if b[b_ind % l] not in child:
                child[c_ind % l] = b[b_ind % l]
                c_ind += 1
            b_ind += 1
        return child

    @genetic_operation('crossover')
    def partially_mapped_crossover(self, ch_indices):
        if len(ch_indices) != 2 or not all( i < n for i in ch_indices):
           raise SrflpError(f'Indices of genes are empty or exceed upper limit {ch_indices}')
        chr_a,chr_b = self.population[ch_indices[0]],self.population[ch_indices[1]]
        half = len(chr_a.F) // 2
        a = random.randint(0, len(chr_a.F)-half)
        b = a + half
        print(a,b)
        print(chr_a.F, chr_b.F)
        return self.pmx(chr_a,chr_b,a,b),self.pmx(chr_b,chr_a,a,b)

    @genetic_operation('crossover')
    def order_crossover(self, ch_indices):
        if len(ch_indices) != 2 or not all( i < n for i in ch_indices):
           raise SrflpError(f'Indices of genes are empty or exceed upper limit {ch_indices}')
        chr_a,chr_b = self.population[ch_indices[0]],self.population[ch_indices[1]]
        half = len(chr_a.F) // 2
        a = random.randint(0, len(chr_a.F)-half)
        b = a + half
        print(a,b)
        print(chr_a.F, chr_b.F)
        return self.ox(chr_a,chr_b,a,b),self.pmx(chr_b,chr_a,a,b)


    def __str__(self):
        return '\n'.join([str(x) for x in self.population])

if __name__ == "__main__":
    N = 10**6
    n = 6
    L = [20, 10, 16, 20, 10, 10]
    C = [
            [-1, 12, 3, 6, 0, 20],
            [12, -1, 5, 5, 5, 0],
            [3, 5, -1, 10, 4, 2],
            [6, 5, 10, -1, 2, 12],
            [0, 5, 4, 2, -1, 6],
            [20, 0, 2, 12, 6, -1]
        ]
    pop = Population([SrflpChromosome(n,L,C), SrflpChromosome(n,L,C), SrflpChromosome(n,L,C), SrflpChromosome(n,L,C)])
    # print(pop.selection_rank(2))
    # print(pop.selection_rand(2))
    pop.swap_mutation([0,1],2)
    # pop.insert_mutation([0,1])
    # pop.scramble_mutation([0,1])
    # pop.reverse_mutation([0,1])
    # print(pop.partially_mapped_crossover([0,1]))
    print(pop.order_crossover([0,1]))