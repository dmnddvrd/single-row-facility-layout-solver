require('dotenv').config();

const jwt = require('jsonwebtoken'),
  userDao = require('../db/repositories/users'),
  hasher = require('../util/pwd-hasher');
// Controller func of POST: /users/create
exports.createUser = (form) => {
  const {
    name, username, email,
  } = form;
  if (form.password === '' || name === '' || username === '') {
    return false;
  }
  const password = hasher.hash(form.password);
  return userDao.addUser(name, username, email, password);
};

// Controller func of POST: /users/delete
exports.removeUser = (form) => {
  const id = parseInt(form.id, 10);
  if (Number.isNaN(id)) {
    return false;
  }
  return userDao.deleteUser(id);
};

// Controller func of GET: /users/all
exports.queryUsers = async (form) => {
  const { username, email } = form;

  // Find by username:
  if (username !== undefined && username !== '') {
    const response = await userDao.findUser([['username', '=', username]]);
    return response;
  }

  // Find by email:
  if (email !== undefined && email !== '') {
    const response = await userDao.findUser([['email', '=', email]]);
    return response;
  }

  // Find all:
  const response = await userDao.getUsers();
  return response;
};


// Controller func of POST: /users/login
exports.authenticateUser = async (form) => {
  const { username, email } = form;
  let user = [];
  // Find by username if non-empty username/email has been provided:
  if (username !== undefined && username !== '') {
    user = await userDao.findUser([['username', '=', username]]);
  } else if (email !== undefined && email !== '') {
    user = await userDao.findUser([['email', '=', email]]);
  }
  // If user has not been found
  if (Object.keys(user).length === 0 || !hasher.compare(form.password, user[0].password)) {
    return false;
  }
  [user] = user;
  return {
    token: jwt.sign({
      username,
      email,
    }, process.env.JWT_TOKEN, { expiresIn: '1h' }),
    user,
  };
};
