const knex = require('knex'),
  knexFile = require('../../../knexfile').development;

const db = knex(knexFile);

const insertData = (tableName, data) => db(tableName)
  .insert(data)
  .then((resp) => resp)
  .catch((error) => console.log(error));


const selectData = (tableName, options = { fields: [], filteringConditions: [] }) => {
  const { fields, filteringConditions } = options;

  return db(tableName)
    .select(fields)
    .where((builder) => {
      filteringConditions.forEach((condition) => {
        builder.where(...condition);
      });
    })
    .orderBy('id')
    .then((data) => data);
};

const deleteData = (tableName, options = { filteringConditions: [] }) => {
  const { filteringConditions } = options;

  return db(tableName)
    .where((builder) => {
      filteringConditions.forEach((condition) => {
        builder.where(...condition);
      });
    })
    .del()
    .then((data) => data);
};

const updateData = (tableName, options = { fields: {}, filteringConditions: [] }) => {
  const { fields, filteringConditions } = options;

  return db(tableName)
    .where((builder) => {
      filteringConditions.forEach((condition) => {
        builder.where(...condition);
      });
    })
    .update(fields)
    .then((data) => data);
};

module.exports = {
  selectData,
  insertData,
  updateData,
  deleteData,
};
