exports.up = (knex) =>  knex.schema.createTable('srflp_problems', (table) => {
    table.increments('id').notNullable();
    table.string('user_id');
    table.integer('generations').unsigned();
    table.string('solution');
    table.integer('population_size').unsigned();
    table.string('mutation_type');
    table.string('crossover_type');
    table.float('p_mutation');
    table.float('p_crossover');
    table.float('fitness_val');
    table.float('init_fitness_val');
    table.float('execution_time');
    table.string('status');
    table.timestamp('created_at').defaultTo(knex.fn.now());
  });
  
  exports.down = (knex) => knex.schema.dropTableIfExists('srlp_problems');
  