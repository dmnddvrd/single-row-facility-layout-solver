const express = require('express'),
  userController = require('../controllers/user-controller'),
  problemController = require('../controllers/problem-controller'),
  validator = require('../util/input-validator'),
  authMW = require('../middleware/user-authentication');

const app = express.Router();

app.get('/all', async (req, res) => {
  const formData  = req.query;
  return res.status(200).json({
    status:'success',
    problems: await problemController.getAllProblems(formData),
  });
});

app.post('/create', async (req, res) => {
  const formData = req.body;
    if (!form.user_id || !form.generations || !form.population_size || !form.mutation_type ||
      !form.crossover_type || !form.p_mutation || !form.p_crossover || ! form.fitness_val) {
        return res.status(400).json({
          status: 'error',
          error: 'req body missing parameters or invalid email format',
        });
  }
  
  const id = await problemController.createProblem(formData);
  if(id === false || id === undefined) {
    return res.status(400).json({
      status: 'error',
      error: 'could not create record',
    });
  }

  return res.status(200).json({
    status: 'success',
    problemId: id[0],
  });
});

module.exports = app;