from random import sample
from srflp.chromosome import Population
import numpy as np
from srflp.exception import SrflpError
import srflp.utils.config as config
import itertools

class SrflpChromosomeGenerator:
 
    MIN_COST = 5
    MAX_COST = 20
    MIN_LENGTH = 4
    MAX_LENGTH = 50

    @classmethod
    def generate_sample(cls, n = 6, sample_size=10**4):
        from srflp.algorithm import SrflpChromosome
        if n<3 or sample_size < 1 or n > cls.MAX_LENGTH-cls.MIN_LENGTH:
            raise SrflpError(f'Incorrect input provided n should be between {cls.MIN_LENGTH} and {cls.MAX_LENGTH}')
        for i in range(sample_size):
            L = sample(range(cls.MIN_LENGTH, cls.MAX_LENGTH), n)
            C = np.random.random_integers(cls.MIN_COST,cls.MAX_COST,size=(n, n))
            C = (C + C.T)/2
            for i in range(n):
                C[i][i] = -1
            C = C.tolist()
            yield SrflpChromosome(n, L, C)