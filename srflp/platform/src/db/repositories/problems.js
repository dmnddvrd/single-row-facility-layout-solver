const repo = require("./repo");

exports.addProblem = (
  user_id,
  generations,
  population_size,
  mutation_type,
  crossover_type,
  p_mutation,
  p_crossover,
  srflp_json,
  fitness_val = 0,
  execution_time = 0,
  status = "In Progress"
) =>
  repo
    .insertData("srflp_problems", [
      {
        user_id,
        generations,
        solution: "",
        population_size,
        mutation_type,
        crossover_type,
        p_mutation,
        p_crossover,
        srflp_json,
        fitness_val,
        execution_time,
        status,
      },
    ])
    .then((id) => {
      console.log(`Record ${id} inserted into "srflp_problems" table.`);
      return id;
    })
    .catch((err) => {
      console.log(err);
    });

exports.getProblems = () =>
  repo
    .selectData("srflp_problems", {
      filteringConditions: [],
    })
    .then((problems) => {
      console.log(
        `Queried nr of records from "users" table: ${problems.length}`
      );
      return problems;
    });

exports.getUsersProblems = (id) =>
  repo
    .selectData("srflp_problems", {
      filteringConditions: [["user_id", "=", id]],
    })
    .then((problems) => {
      console.log(
        `Queried nr of records from "users" table: ${problems.length}`
      );
      return problems;
    });

exports.updateProblem = (id, user_id) => {
  repo
    .updateData("srflp_problems", {
      filteringConditions: [
        ["user_id", "=", user_id],
        ["id", "=", id],
      ],
      fields: { status: "Stopped" },
    })
    .then((problem) => {
      console.log(`Updated row ${problem}`);
      return problem;
    });
};
