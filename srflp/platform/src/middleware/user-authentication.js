require('dotenv').config();

const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
  // Requiring all signed cookies
  const cookies = req.signedCookies;
  let errMsg = '';
  if (cookies) {
    // const cookiesJson = JSON.stringify(cookies);
    // console.log(`Signed Cookies: ${cookiesJson}`);
    const accessToken = cookies.jwt_token;
    // If cookie contains a valid token => he's already logged in
    jwt.verify(accessToken, process.env.JWT_TOKEN, (err, payload) => {
      if (err) {
        errMsg = 'could not authenticate';
      }
      if (payload) {
        const payloadJson = JSON.stringify(payload);
        console.log(`Payload: ${payloadJson}`);
      } else {
        errMsg = 'log in first';
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
