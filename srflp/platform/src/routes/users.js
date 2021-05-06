const express = require('express'),
  userController = require('../controllers/user-controller'),
  validator = require('../util/input-validator'),
  authMW = require('../middleware/user-authentication');

const app = express.Router();

app.get('/all', async (req, res) => {
  const formData = req.query;
  return res.status(200).json({
    status: 'success',
    users: await userController.queryUsers(formData),
  });
});

app.post('/create', async (req, res) => {
  const formData = req.body;
  if (!formData.name || !formData.username || !formData.email
    || !formData.password || !validator.isValidEmail(formData.email)) {
    return res.status(400).json({
      status: 'error',
      error: 'req body missing parameters or invalid email format',
    });
  }
  const id = await userController.createUser(formData);
  if (id === false || id === undefined) {
    return res.status(400).json({
      status: 'error',
      error: 'could not create record',
    });
  }
  return res.status(200).json({
    status: 'success',
    // user: req.signedCookies.user,
    userId: id[0],
  });
});

app.post('/login', async (req, res) => {
  const formData = req.body;
  const { username, email, password } = formData;
  if (!(username || email) || !password) {
    return res.status(400).json({
      status: 'error',
      error: 'req body missing parameters',
    });
  }
  const resp = await userController.authenticateUser(formData);
  if (!resp) {
    return res.status(400).json({
      status: 'error',
      error: 'could not authenticate user',
    });
  }
  res.cookie('user', { id: resp.user.id, username, email }, { signed: true });
  res.cookie('jwt_token', resp.token, { signed: true });
  return res.status(200).json({
    status: 'success',
    token: resp.token,
  });
});

app.use(authMW);

app.post('/delete', async (req, res) => {
  const formData = req.body;
  if (!formData.id) {
    return res.status(400).json({
      status: 'error',
      error: 'req body missing id parameter',
    });
  }
  const resp = await userController.removeUser(formData);
  if (!resp) {
    return res.status(400).json({
      status: 'error',
      error: `could not delete record ${formData.id}`,
    });
  }
  return res.status(200).json({
    status: 'success',
    // user: req.signedCookies.user,
    deleted: formData.id,
  });
});

module.exports = app;
