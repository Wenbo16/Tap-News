// Client is a Lynx StatsD client
function statSdFactory(client) {
    return function(options) {
        options = options || {};
        var timeByUrl = options.timeByUrl || false;

        return function(req, res, next) {
            var startTime = new Date();
            var endTime;

            // Shadow end request
            var end = res.end;
            res.end = function() {
                end.apply(res, arguments);

                client.increment('response_code.' + res.statusCode);

                // Time by URL?
                if (timeByUrl) {
                    var routeName = "unknown_express_route";

                    // Did we get a harc-coded name, or should we figure one out?
                    if (res.locals && res.locals.statsdUrlKey) {
                        routeName = res.locals.statsdUrlKey;
                    } else if (req.route && req.route.path) {
                        routeName = req.route.path;
                        if (Object.prototype.toString.call(routeName) === '[object RegExp]') {
                            // Might want to do some sanitation here?
                            routeName = routeName.source;
                        }
                        if (routeName === "/") {
                            routeName = "root";
                        }
                        routeName = req.method + '_' + routeName;
                    } else if (req.url) { // Required to pickup static routes
                        routeName = req.method + '_' + req.url;
                    }

                    // Get rid of : in route names, remove first and last /,
                    // and replace rest with _.
                    routeName = routeName.replace(/:/g, "").replace(/^\/|\/$/g, "").replace(/\//g, "_");
                    endTime = new Date();
                    client.timing('response_time.' + routeName, endTime - startTime);
                    client.increment("requests." + routeName);
                } else {
                    endTime = new Date();
                    client.timing('response_time', endTime - startTime);
                }
            };
            next();
        };
    };
}

module.exports = statSdFactory;
