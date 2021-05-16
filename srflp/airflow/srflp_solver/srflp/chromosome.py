from srflp.exception import SrflpError

# Permutational representation of a Chromosome
# Ex: For n = 4 can be [0,1,2,3], [0,3,2,1], etc.
class Chromosome:

    MIN_N = 2
    MAX_N = 100

    def __init__(self, n, F = None):
        if n < 2 or n > self.MAX_N:
            raise SrflpError(f'Incorrect input for table provided (n={n} should be between {self.MIN_N} and {self.MAX_N})')
        self.F = [x for x in range(n)] if not F else F

    def mutate(self, algorithm):
        print(f'Mutating chromosome {self.f} using {algorithm}')

    def crossover(self, other: "Chromosome"):
        print(f'Creating crossover from {self.F} and {other.F}')