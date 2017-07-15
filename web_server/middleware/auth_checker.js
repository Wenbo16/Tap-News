const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../../config/config.json');
const log = require('../logging/log');


module.exports = (req, res, next) => {
    log.info({req: req}, 'something about handling this request'+req.email);

    if (!req.headers.authorization) {
        return res.status(401).end();
    }

    // get the last part from a authorization header string like "bearer token-value"
    const token = req.headers.authorization.split(' ')[1];

    // console.log('auth_checker: token: ' + token);

    // decode the token using a secret key-phrase
    return jwt.verify(token, config.web_server.auth_checker.jwtSecret, (err, decoded) => {
        // the 401 code is for unauthorized status
        if (err) {
            log.info({err:err});
            return res.status(401).end();
        }

        const id = decoded.sub;

        // check if a user exists
        return User.findById(id, (userErr, user) => {
            if (userErr || !user) {
                log.info({err:userErr}, 'user does not exit');
                return res.status(401).end();
            }

            return next();
        });
    });
};