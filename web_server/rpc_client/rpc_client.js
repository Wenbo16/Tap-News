var jayson = require('jayson');
const log = require('../logging/log');
const config = require('../../config/config.json');

const port = config.web_server.rpc_client.port;
const hostname = config.web_server.rpc_client.hostname;

var client = jayson.client.http({
	port,
	hostname
});

// Test RPC method
function add(a, b, callback) {
	client.request('add', [a, b], function(err, error, response) {
		if (err) throw err;
		callback(response);
	});
}

// Get news summaries for a user
function getNewsSummariesForUser(user_id, page_num, callback) {
	client.request('getNewsSummariesForUser', [user_id, page_num], function(err, error, response) {
		if (err) {
			log.error({err,err});
			throw err;
		}
		callback(response);
	});
}

// Log a news click event for a user
function logNewsClickForUser(user_id, news_id) {
	client.request('logNewsClickForUser', [user_id, news_id], function(err, error, response) {
		if (err) {
			log.error({err,err});
			throw err;
		}
	});
}

// get similar news
function getSimilarNews(user_id, news_id, callback){
	client.request('getSimilarNews', [user_id, news_id], function(err, error, response){
		if (err) {
			log.error({err,err});
			throw err;
		}
		console.log(response);
		callback(response);
	});
}


module.exports = {
	add: add,
	getNewsSummariesForUser: getNewsSummariesForUser,
	logNewsClickForUser: logNewsClickForUser,
	getSimilarNews: getSimilarNews
};