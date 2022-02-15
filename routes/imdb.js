/**
 * @swagger
 * /imdb:
 *   get:
 *     summary: Retrieve a rating from an IMDB movie
 *     description: Retrieve a rating from an IMDB movie
*/

const express = require('express');
const router = express.Router();

// returns the rating of an input movie from IMDB
router.get('/', (req, res) => {
    req = req.query;
    var movie = req.movie;
    var url = 'http://www.omdbapi.com/?t=' + movie + '&apikey=thewdb';
    var request = require('request');
    request(url, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            var json = JSON.parse(body);
            var rating = json.imdbRating;
            res.send(rating);
        }
    });
});

