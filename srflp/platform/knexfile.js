require('dotenv').config();

module.exports = {
  development: {
    client: 'mysql',
    connection: {
      host: process.env.DB_PORT,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
    },
    seeds: {
      directory: './src/db/seeds/',
    },
    migrations: {
      directory: './src/db/migrations/',
    },
  },
};
