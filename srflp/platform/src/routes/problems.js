const express = require("express"),
  userController = require("../controllers/user-controller"),
  problemController = require("../controllers/problem-controller"),
  validator = require("../util/input-validator"),
  authMW = require("../middleware/user-authentication");

const app = express.Router();

app.get("/all", async (req, res) => {
  const formData = req.query;
  return res.status(200).json({
    status: "success",
    problems: await problemController.getAllProblems(formData),
  });
});

app.post("/stop", async (req, res) => {
  let form = req.body;
  if (!form.id) {
    return res.status(400).json({
      status: "error",
      error: "req body missing problem id",
    });
  }
  form.user_id = req.signedCookies.user.id;
  const id = problemController.stopProblem(form);
  console.log(id);
  // if (id === false || id === undefined) {
  //   return res.status(400).json({
  //     status: "error",
  //     error: "could not update record",
  //   });
  // }

  return res.status(200).json({
    status: "success",
    problemId: id[0],
  });
});

app.post("/create", async (req, res) => {
  let form = req.body;
  if (
    !form.number_of_generations ||
    !form.population_size ||
    !form.mutation_type ||
    !form.crossover_type ||
    !form.probability_of_mutation ||
    !form.probability_of_crossover ||
    !form.srflp_json
  ) {
    return res.status(400).json({
      status: "error",
      error: "req body missing parameters",
    });
  }
  form.user_id = req.signedCookies.user.id;
  const id = await problemController.createProblem(form);
  if (id === false || id === undefined) {
    return res.status(400).json({
      status: "error",
      error: "could not create record",
    });
  }

  return res.status(200).json({
    status: "success",
    problemId: id[0],
  });
});

module.exports = app;
