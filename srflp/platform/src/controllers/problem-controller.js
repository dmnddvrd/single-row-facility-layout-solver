require('dotenv').config();

const jwt = require('jsonwebtoken'),
  userDao = require('../db/repositories/users'),
  problemDao = require('../db/repositories/problems'),
  hasher = require('../util/pwd-hasher');

exports.createProblem = (form) => {
    const {
        user_id, generations, population_size, mutation_type, crossover_type,
        p_mutation, p_crossover, fitness_val
    } = form;
    const execution_time = 0;
    const status = 'New';
    if (!form.user_id || !form.generations || !form.population_size || !form.mutation_type ||
        !form.crossover_type || !form.p_mutation || !form.p_crossover || ! form.fitness_val) {
        return false;
    }
    return problemDao.addProblem(user_id, generations, population_size, mutation_type, p_mutation,
        p_crossover, fitness_val, execution_time, status);
}

exports.getAllProblems  = async (form) => {
    const resp = await problemDao.getProblems();
    return resp;
}

exports.getUsersProblems = async (form) => {
    const { user_id } = form;
    const resp = await problemDao.getUsersProblems(user_id);
    return resp;
}
