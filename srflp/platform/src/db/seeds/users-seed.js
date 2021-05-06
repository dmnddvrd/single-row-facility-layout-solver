
const hasher = require('../../util/pwd-hasher');

// 0. role -> owner
// 1. role -> admin
// 2. role -> basic user

exports.seed = (knex) => knex('users').del()
  .then(() => knex('users').insert([
    {
      id: 1, name: 'Dimand Edvard', username: 'root', email: 'deim1612@srflp.com', password: hasher.hash('root'), role: 0,
    },
    {
      id: 2, name: 'Admin Janos', username: 'jani', email: 'jani@srflp.com', password: hasher.hash('password1234'), role: 1,
    },
    {
      id: 3, name: 'Guest Pista', username: 'pista', email: 'pista@srflp.com', password: hasher.hash('password1234'), role: 2,
    },
    {
      id: 4, name: 'Guest Benedek', username: 'benedek', email: 'benedek@srflp.com', password: hasher.hash('password1234'), role: 2,
    },
  ]));
