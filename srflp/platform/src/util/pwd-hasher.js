const bcrypt = require('bcrypt');

exports.hash = (input) => bcrypt.hashSync(input, bcrypt.genSaltSync(9));

exports.compare = (a, b) => bcrypt.compareSync(a, b);
