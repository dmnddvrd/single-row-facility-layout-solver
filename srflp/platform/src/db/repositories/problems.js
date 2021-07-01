const repo = require('./repo');

exports.addProblem = (
    user_id, generations, population_size, mutation_type, p_mutation, p_crossover, fitness_val = 0, execution_time = 0, status = 'Unsolved'
) => repo.insertData('srflp_problems', [{
    user_id, generations, population_size, mutation_type, p_mutation, p_crossover, fitness_val, execution_time, status
}]).then((id) => {
    console.log(`Record ${id} inserted into "srflp_problems" table.`);
    return id;
});

exports.getProblems = () => repo.selectData('srflp_problems',{
    filteringConditions: [],
})
.then((problems) => {
    console.log(`Queried nr of records from "users" table: ${problems.length}`);
    return problems;
});

exports.getUsersProblems = (id) => repo.selectData('srflp_problems', {
    filteringConditions: [
        ['user_id', '=' , id]
    ],
})
.then((problems) =>{
    console.log(`Queried nr of records from "users" table: ${problems.length}`);
    return problems;
});