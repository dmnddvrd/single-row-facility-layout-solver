require('dotenv').config();
const express = require('express'),
  session = require('express-session'),
  cookieParser = require('cookie-parser'),
  path = require('path'),
  morgan = require('morgan'),
  bodyParser = require('body-parser'),
  problemRouter = require('./src/routes/problems'),
  usersRouter = require('./src/routes/users');


const app = express(),
  staticDir = path.join(__dirname, 'static'),
  port = 8080;

app.use(cookieParser(process.env.COOKIE_SECRET));

app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: true,
}));

// Using the logging from the example lab
app.use(morgan('tiny'));

// Serving static library
app.use(express.static(staticDir));

// To parse the body
app.use(bodyParser.urlencoded({ extended: true }));

// Setting up handlebars
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'views'));

app.disable('etag');


app.use('/users', usersRouter);
app.use('/problems', problemRouter);

app.get('/admin', async (req, res) => {
  let email;
  if (req.signedCookies.user) {
    email = req.signedCookies.user.email;
  }
  res.render('admin', { name: email });
});

app.get(['/', '/index'], async (req, res) => {
  let email;
  if (req.signedCookies.user) {
    email = req.signedCookies.user.email;
  }
  res.render('index', { name: email });
});

app.get('/login', async (req, res) => {
  if (req.signedCookies.jwt_token) {
    res.render('index', { name: req.signedCookies.user.email });
  }
  res.render('login');
});

app.all('/logout', async (req, res) => {
  res.clearCookie('jwt_token');
  res.clearCookie('user');
  res.render('login');
});

app.get('/register', async (_req, res) => {
  res.render('register');
});


app.get('*', (_req, res) => {
  res.render('error',  {});
});

app.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}/...`);
});


require('hbs').registerHelper('ifDefined', (name, options) => {
  if (name !== '' && name !== undefined) {
    return options.fn(name);
  }
  return options.inverse(this);
});
