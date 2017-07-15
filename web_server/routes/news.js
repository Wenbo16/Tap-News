var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();
const log = require('../logging/log');
// const User = require('mongoose').model('User');


/* GET news list. */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
	log.info('Fetching news...');
	console.log('Fetching news...');
	user_id = req.params['userId'];
	page_num = req.params['pageNum'];

	rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
		res.json(response);
	});
});

/* Log news click. */
router.get('/userId/:userId/newsId/:newsId', function(req,res,next) {
	log.info('Logging news click...');
	console.log('Logging news click...');
	user_id = req.params['userId'];
	news_id = req.params['newsId'];

	rpc_client.logNewsClickForUser(user_id, news_id);
	rpc_client.getSimilarNews(user_id, news_id, function(response){
		res.json(response);
	});
});


/* get user likes */
router.post('/userLikes/userId/:userId/newsId/:newsId', function(req,res,next) {
	log.info('Logging user add likes...');
	console.log('Logging user add likes...');
	user_id = req.params['userId'];
	news_id = req.params['newsId'];
	res.status(200);
});


module.exports = router;