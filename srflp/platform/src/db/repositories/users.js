const repo = require('./repo');

exports.getUsers = () => repo.selectData('users', {
  filteringConditions: [],
})
  .then((users) => {
    console.log(`Queried nr of records from "users" table: ${users.length}`);
    return users;
  });

exports.findUser = (filteringConditions) => repo.selectData('users', {
  filteringConditions,
}).then((user) => {
  const info = JSON.stringify(user);
  console.log(`User found: ${info}`);
  return user;
});

exports.addUser = (name, username, email, password, role = 2) => repo.insertData('users', [
  {
    name,
    username,
    email,
    password,
    role,
  },
])
  .then((insertedId) => {
    console.log(`Record ${insertedId} inserted into "users" table`);
    return insertedId;
  });


exports.deleteUser = (id) => repo.deleteData('users', {
  filteringConditions: [
    ['id', '=', id],
  ],
})
  .then((deletedId) => {
    console.log(`Deleted user: ${deletedId}`);
    return deletedId > 0;
  });
