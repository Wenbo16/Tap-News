const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../../config/config.json');
const log = require('../logging/log');


// The local authentication strategy authenticates users using a username and password. 

module.exports = new PassportLocalStrategy({
	// Both fields define the name of the properties in the POST body that are sent to the server.
	// By default, LocalStrategy expects to find credentials in parameters named username and password.
	// If your prefers to name these fields differently, options are available to change the defaults.
	usernameField: 'email',
	passwordField: 'password',
	passReqToCallback: true

// The strategy requires a verify callback, which accepts these credentials and calls done providing a user.
}, (req, email, password, done) => {
		const userData = {
			email: email.trim(),
			password: password.trim()
		};

		// find a user by email address
		return User.findOne({
			email: userData.email
		}, (err, user) => {
			if (err) {
				log.info({err:err});
				return done(err);
			}

			// if no user in database
			if (!user) {
				const error = new Error('Incorrect email or password');
				error.name = 'IncorrectCredentialsError';
				log.info({err:error}, 'Incorrect email or password');
				// return done(null, false, { message: 'Incorrect username.' });
				return done(error);
			}

			log.info({user:user},'User login');
			// if user in database
			// check if a hashed user's password is equal to a value saved in the database
			return user.comparePassword(userData.password, (passwordErr, isMatch) => {
				if (err) {
					return done(err);
				}

				if (!isMatch) {
					const error = new Error('Incorrect email or password');
					error.name = 'IncorrectCredentialsError';
					log.info({err:error}, 'Incorrect email or password');
					return done(error);
				}

				const payload = {
					sub: user._id
				};

				// create a token string
				const token = jwt.sign(payload, config.web_server.login_password.jwtSecret);
				const data = {
					name: user.email
				};

				return done(null, token, data);
			});
		});
});