const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const log = require('../logging/log');


module.exports = new PassportLocalStrategy({
	usernameField: 'email',
	passwordField: 'password',
	passReqToCallback: true
}, (req, email, password, done) => {
	const userData = {
		email: email.trim(),
		password: password.trim(),
	};

	const newUser = new User(userData);
	newUser.save((err) => {
		log.info({user:UserData},'Save new user!');
		if (err) {
			log.error({err:err});
			return done(err);
		}

		return done(null);
	});
});