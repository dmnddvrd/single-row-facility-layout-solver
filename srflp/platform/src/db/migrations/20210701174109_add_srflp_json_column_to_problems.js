exports.up = function (knex) {
  return knex.schema.table("srflp_problems", (table) => {
    table.json("srflp_json");
  });
};

exports.down = function (knex) {
  return knex.schema.table("srflp_problems", (table) => {
    table.dropColumn("srflp_json");
  });
};
