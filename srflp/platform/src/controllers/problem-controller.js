require("dotenv").config();

const jwt = require("jsonwebtoken"),
  userDao = require("../db/repositories/users"),
  problemDao = require("../db/repositories/problems"),
  hasher = require("../util/pwd-hasher");

exports.createProblem = (form) => {
  const {
    user_id,
    number_of_generations,
    population_size,
    mutation_type,
    crossover_type,
    probability_of_mutation,
    probability_of_crossover,
    fitness_val,
    srflp_json,
  } = form;
  const execution_time = 0;
  const status = "In Progress";
  if (
    !form.number_of_generations ||
    !form.population_size ||
    !form.mutation_type ||
    !form.crossover_type ||
    !form.probability_of_mutation ||
    !form.probability_of_crossover ||
    !form.srflp_json
  ) {
    return false;
  }
  return problemDao.addProblem(
    user_id,
    number_of_generations,
    population_size,
    mutation_type,
    crossover_type,
    probability_of_mutation,
    probability_of_crossover,
    srflp_json,
    fitness_val,
    execution_time,
    status
  );
};

exports.stopProblem = async (form) => {
  const resp = await problemDao.updateProblem(form.id, form.user_id);
  return resp;
};

exports.getAllProblems = async (form) => {
  const resp = await problemDao.getProblems();
  return resp;
};

exports.getUsersProblems = async (form) => {
  const { user_id } = form;
  const resp = await problemDao.getUsersProblems(user_id);
  return resp;
};
