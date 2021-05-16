import json
from srflp.exception import SrflpError
from srflp.chromosome import Chromosome

class SrflpTable(Chromosome):

    MIN_N = 2
    MAX_N = 100

    def __str__(self):
        return json.dumps({
            'n': self.n,
            'F': self.F,
            'L': self.L,
            'C': self.C,
        })

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
        
    def get_distance(self, i, j)->float:
        sum = 0
        if i > j:
            i,j = j,i
        for k in self.F[i+1:j]:
            sum = sum + self.L[k]
        distance = (self.L[i] + self.L[j]) / 2 + sum
        return distance

    def get_fitness(self)->float:
        sum = 0
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                if i != j:
                    sum = sum + self.C[i][j] * self.get_distance(i, j)
        return sum 