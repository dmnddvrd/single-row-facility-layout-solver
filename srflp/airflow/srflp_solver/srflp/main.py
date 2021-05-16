from srflp.data.generator import SrflpTableGenerator
from srflp.algorithm import SrflpAlgorithm
from srflp.table import SrflpTable

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
    x = SrflpTable(n,L,C)
    SrflpAlgorithm.solve_simple(x, N, 'brute_force')
    
# def main():
#     for n in range(49,50):
#         for table in SrflpTableGenerator.generate_sample(19):
#             SrflpAlgorithm.solve_simple(table, 100, 'brute_force')
#             SrflpAlgorithm.solve_simple(table, 100, 'RANDOM_PERMUTATION')
        
if __name__ == "__main__":
    main()