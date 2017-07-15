const mongoose = require('mongoose');
var log = require('../logging/log');

module.exports.connect = (uri) => {
	mongoose.connect(uri);

	mongoose.connection.on('error', (err) => {
		log.error({err:err}, 'Mongoose connection error')
		process.exit(1);
	});

	// load models
	require('./user');
};