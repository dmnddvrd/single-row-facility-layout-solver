
const jwt = require('jsonwebtoken');
// Checking whether has admin role
module.exports = (req, res, next) => {
  const cookies = req.signedCookies;
  let errMsg = '';
  if (cookies) {
    jwt.verify(cookies.jwt_token, process.env.JWT_TOKEN, (err, payload) => {
      if (err) {
        errMsg = 'could not authenticate';
      }
      if (payload && payload.role && payload.role < 2) {
        const info = JSON.stringify(payload);
        console.log(`Payload: ${info}`);
      } else {
        errMsg = 'you dont have the neccessary privileges';
      }
    });
  } else {
    return res.status(400).json({
      status: 'error',
      error: 'log in first',
    });
  }
  if (errMsg !== '') {
    return res.status(400).json({
      status: 'error',
      error: errMsg,
    });
  }
  return next();
};
