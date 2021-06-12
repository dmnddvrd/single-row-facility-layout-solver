from srflp.data.generator import SrflpChromosomeGenerator
from srflp.algorithm import SrflpAlgorithm
from srflp.chromosome import SrflpChromosome, Chromosome, Population

def main():
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
    # x = SrflpChromosome(n,L,C)
    # pop = Population([x,x,x,x])
    # SrflpAlgorithm.solve_simple(x, 10000, 'brute_force')
    # SrflpAlgorithm.solve_simple(x, 10000, 'RANDOM_PERMUTATION')
def main():
    for n in range(5,50):
        for chromosome in SrflpChromosomeGenerator.generate_sample(n):
            SrflpAlgorithm.solve_simple(chromosome, 100, 'brute_force')
            SrflpAlgorithm.solve_simple(chromosome, 100, 'RANDOM_PERMUTATION')
        
if __name__ == "__main__":
    main()


def generate_test_data():
        for n in range(5,50):
            chromosomes = []
            for chromosome in SrflpChromosomeGenerator.generate_sample(n, ):
                SrflpAlgorithm.solve_simple(chromosome, 100, 'brute_force')
                chromosomes.append(chromosome)

# BRUTE_FORCE: Best solution from 720 iterations took 29 steps -> (0, 2, 1, 5, 3, 4) -> 2846.0
# Function brute_force execution time: 0.011421442031860352
# Using alogirthm RANDOM_PERMUTATION
# RANDOM PERM: Best solution from 10000 iterations took 28 steps -> [1, 4, 3, 5, 0, 2] -> 2846.0
# Function random_permutations execution time: 0.17294716835021973
# airflow@3b6e6e3ea7c9:~/srflp-solver/srflp$ python main.py
# Using alogirthm BRUTE_FORCE
# BRUTE_FORCE: Best solution from 720 iterations took 29 steps -> (0, 2, 1, 5, 3, 4) -> 2846.0
# Function brute_force execution time: 0.010756254196166992
# Using alogirthm RANDOM_PERMUTATION
# RANDOM PERM: Best solution from 10000 iterations took 36 steps -> [0, 4, 1, 3, 2, 5] -> 2846.0
# Function random_permutations execution time: 0.1765117645263672
# airflow@3b6e6e3ea7c9:~/srflp-solver/srflp$ python main.py
# Using alogirthm BRUTE_FORCE
# BRUTE_FORCE: Best solution from 720 iterations took 29 steps -> (0, 2, 1, 5, 3, 4) -> 2846.0
# Function brute_force execution time: 0.010523557662963867
# Using alogirthm RANDOM_PERMUTATION
# RANDOM PERM: Best solution from 10000 iterations took 35 steps -> [3, 4, 1, 2, 0, 5] -> 2846.0