import os, math, csv, time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from datetime import date
from srflp.data.generator import SrflpChromosomeGenerator
from srflp. algorithm import SrflpAlgorithm

def generate_solutions_data():
    for n in range(10,50):
        solution_data = []
        for chromosome in SrflpChromosomeGenerator.generate_sample(n, sample_size = 10):
            start_time = time.time()
            (sol_chrom, total_iterations, sol_iteration, order_of_genes, fitness_val) = SrflpAlgorithm.solve_simple(chromosome, 1_000_000, 'brute_force')
            time_delta = str((time.time() - start_time))[:6]
            solution_data.append([n, sol_iteration, total_iterations, order_of_genes, fitness_val, time_delta, str(sol_chrom)])
        header = ['n','sol_iteration', 'total_iterations', 'order_of_genes','fitness_val','execution_time','sol_chrom_json',]
        with open(os.path.abspath(f'./solutions_{str(date.today())}.csv'), 'a') as f:
            writer = csv.writer(f)
            writer.writerows(solution_data)

def get_brute_force_exec_time():
    df = pd.read_csv('./solutions/solutions_2021-06-12.csv')
    execution_time_data = df.groupby('n', as_index=False)['execution_time'].mean()
    fig, ax = plt.subplots()
    ax.plot(execution_time_data['n'], execution_time_data['execution_time'])
    ax.set(xlabel='egyed mérete(n)', ylabel='futási idő (s)', title='Brute force megközeltítés futási ideje')
    ax.xaxis.set_ticks(np.arange(5, 15, 1))
    ax.yaxis.set_ticks(np.arange(0,100, 5))
    ax.grid()
    fig.savefig('./charts/brute_force_exec_time.png')


def get_brute_force_iterations():
    fig, ax = plt.subplots()
    ax.plot(list(range(5,16)), [math.factorial(x) for x in list(range(5,16))])
    # 1_307_674_368_000
    ax.set(xlabel='egyed mérete(n)', ylabel='szükséges iterációk (n!)', title='Iterációk száma egyed mértetétől függően')
    ax.xaxis.set_ticks(np.arange(5, 15, 1))
    ax.grid()
    fig.savefig('./charts/brute_force_iterations.png')

def get_exec_time_by_n():
    df = pd.read_csv('./solutions/solutions_GA.csv')
    exec_time_by_chromosome_size = df.groupby('n', as_index=False)['execution_time'].mean()
    fig, ax = plt.subplots()
    ax.plot(exec_time_by_chromosome_size['n'], exec_time_by_chromosome_size['execution_time'])
    ax.set(xlabel='egyed mérete(n)', ylabel='futási idő (s)', title='GA megközeltítés futási ideje')
    ax.grid()
    fig.savefig('./charts/ga_exec_by_n.png')


def get_err_by_n():
    df = pd.read_csv('./solutions/solutions_GA.csv')
    err_by_n = df.groupby('n', as_index=False)['err_percentage'].mean()
    print(err_by_n)
    fig, ax = plt.subplots()
    ax.plot(err_by_n['n'], err_by_n['err_percentage'])
    ax.set(xlabel='egyed mérete(n)', ylabel='futási idő (s)', title='GA megközeltítés hibája')
    ax.grid()
    fig.savefig('./charts/ga_err_by_n.png')
    print(df.groupby(['crossover_type','n'])['err_percentage'].mean())
    print(df.groupby(['p_c','n'])['err_percentage'].mean())
    print(df.groupby(['p_m','n'])['err_percentage'].mean())

    
if __name__ == '__main__':
    # get_brute_force_exec_time()
    # get_brute_force_iterations()
    get_exec_time_by_n()
    get_err_by_n()