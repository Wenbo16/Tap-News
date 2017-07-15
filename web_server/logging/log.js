var bunyan = require('bunyan');
var log = bunyan.createLogger({
    name: 'myserver',
    streams: [
    {
        path: './logs/main.log',
        level: 'error'
    }, 
    {
        path: './logs/main.log',
        level: 'info'
    }],
    
    serializers: {
        req: bunyan.stdSerializers.req,
        res: bunyan.stdSerializers.res
    }
});

module.exports = log;