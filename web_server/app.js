var bodyParser = require('body-parser');
var cors = require('cors');
var express = require('express');
var passport = require('passport');
var path = require('path');
var Lynx = require('lynx');


var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');
var log = require('./logging/log');

var app = express();

var config = require('../config/config.json');

require('./models/main.js').connect(config.web_server.app.mongoDbUri);


// view engine setup
app.set('view engine', 'jade');
app.set('views', path.join(__dirname, '../client/build/'));

app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));
app.use(bodyParser.json());




// load passport strategies
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// TODO: remove this after development is done.
app.use(cors());

app.use('/', index);
app.use('/auth', auth);

// pass the metrics colletor middleware
var metricsColletorMiddleware = require('./middleware/metrics_collector');
var metrics = new Lynx('localhost', 8125, {prefix: 'express'});
var statsdMiddleware = metricsColletorMiddleware(metrics);
app.use(statsdMiddleware({timeByUrl: true}));


// pass the authenticaion checker middleware
const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);
app.use('/news', news);



// catch 404 and forward to error handler
app.use(function(req, res) {
  var err = new Error('Not Found');
  err.status = 404;
  log.error(err);
  res.send('404 Not Found');
});

module.exports = app;