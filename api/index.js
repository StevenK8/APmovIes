const express = require('express');
const imdb = require('./routes/imdb');
const router = express.Router();

module.exports = () => {
    router.use('/imdb',imdb());

    return router;
};
