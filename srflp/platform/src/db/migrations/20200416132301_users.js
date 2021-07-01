
exports.up = (knex) =>  knex.schema.createTable('users', (table) => {
  table.increments('id').notNullable();
  table.string('name');
  table.string('username').unique();
  table.string('email').unique();
  table.string('password');
  table.integer('role').unsigned().defaultTo(2); // 0 => owner 1 => admin 2 => user
  table.timestamp('created_at').defaultTo(knex.fn.now());
});

exports.down = (knex) => knex.schema.dropTableIfExists('users');
