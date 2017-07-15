var client = require('./rpc_client');

// invoke 'add'
client.add(1, 2, function(response) {
	console.assert(response == 3);
});

// invoke "getNewsSummariesForUser"
client.getNewsSummariesForUser('test_user', 2, function(response) {
	console.assert(response != null);
});

// invoke "logNewsClickForUser"
client.logNewsClickForUser('test_user', "69a4GalHIZm9jF0dkpH3GA==\n");