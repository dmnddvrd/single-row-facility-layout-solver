from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
import MySQLdb
import srflp.utils.config as config
from airflow.operators.python_operator import PythonOperator
from srflp.chromosome import SrflpChromosome, Population
import csv, os, time
from datetime import date
import pandas as pd
import json, random
import numpy as np


DB_HOST = config.get("DB_HOST")
DB_USER = config.get("DB_USER")
DB_PASS = config.get("DB_PASSWORD")
DB_SCHEMA = config.get("DB_SCHEMA")


PROBLEMS = []
SOLUTION = []

print("=======================================================")


def get_problems():
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_SCHEMA)
    curs = db.cursor()
    curs.execute('SELECT * FROM srflp_problems where status = "In Progress";')
    for row in curs.fetchall():
        [
            id,
            _user_id,
            generations,
            _sol,
            pop_size,
            mut_type,
            crossover_type,
            p_m,
            p_c,
            _fitness_val,
            _init_fitness_val,
            _execution_time,
            _status,
            _created_at,
            srflp_json,
        ] = row
        try:
            PROBLEMS.append(
                [
                    id,
                    generations,
                    pop_size,
                    mut_type,
                    crossover_type,
                    p_m,
                    p_c,
                    json.loads(srflp_json),
                ]
            )
        except:
            print(f"Error occured processing row #{id}")
            db.cursor().execute(
                f'UPDATE srflp_problems set status = "Invalid" where id = {id}'
            )
            db.commit()
    print(f"Problems collected: {len(PROBLEMS)}")
    db.close()


def solve_ga():
    for problem in PROBLEMS:
        [
            id,
            generations,
            population_size,
            mutation_type,
            crossover_type,
            p_m,
            p_c,
            chr,
        ] = problem
        print(f"Solving Problem #{id}")
        nr_of_crossovers = int(population_size * p_c)
        # Creating an initial population:
        generation = Population()
        # Generating initial random pop.
        start_time = time.time()
        for i in range(population_size):
            generation.add(
                SrflpChromosome(
                    chr["n"],
                    chr["L"][:],
                    [row[:] for row in chr["C"]],
                    np.random.permutation(chr["n"]).tolist(),
                )
            )
        for i in range(generations):
            generation.population = sorted(
                generation.population, key=lambda x: x.fitness
            )
            # Crossover: parents from the top 50% of the population is mating
            for i in range(nr_of_crossovers):
                parent1 = random.choice(
                    generation.population[: int(population_size / 2)]
                )
                parent2 = random.choice(
                    generation.population[: int(population_size / 2)]
                )
                generation.add(parent1.crossover(parent2, crossover_type))
                generation.add(parent2.crossover(parent1, crossover_type))
            # Mutation: Each individual has a p_m chance to mutate
            for chr in generation.population:
                if random.uniform(0, 1) < p_m:
                    chr.mutation(mutation_type)
            # generation.population = sorted(generation.population, key = lambda x:x.fitness)
            generation.population = random.choices(
                generation.population,
                weights=[x.fitness for x in generation.population],
                k=population_size,
            )
        time_delta = float(time.time() - start_time)
        time_delta_str = str(time_delta)[:6]
        SOLUTION.append(
            [
                id,
                generation.population[-1].fitness,
                generation.population[-1].F,
                time_delta_str,
            ]
        )
        print(f"Problems solved: {len(SOLUTION)}")


def update_problems():
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_SCHEMA)
    for sol in SOLUTION:
        [id, fitness, F, exec_time] = sol
        db.cursor().execute(
            f'UPDATE srflp_problems set status = "Finished", execution_time={exec_time}, fitness_val={fitness},solution="{F}" where id = {id} and status="In Progress";'
        )
        db.commit()
        print(f"Inserted solution for {id} -> {F} (runtime exec_times)")
        db.close()


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["edi.dimand@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=20),
    "execution_timeout": timedelta(seconds=18000),
}


dag = DAG(
    "genetic_algorithm",
    default_args=default_args,
    description="An srlfp solver dag using permutations",
    schedule_interval=timedelta(hours=1),
    start_date=days_ago(1),
    tags=["srflp-solver"],
)

collect_problems = PythonOperator(
    task_id="collect_problems",
    python_callable=get_problems,
    dag=dag,
)

solve_problems = PythonOperator(
    task_id="solve_problems",
    python_callable=solve_ga,
    dag=dag,
)

update_rows = PythonOperator(
    task_id="update_rows",
    python_callable=update_problems,
    dag=dag,
)

collect_problems >> solve_problems >> update_rows
