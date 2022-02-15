const express = require('express');
// const router = express.Router();
const app = express();
// Add swagger
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');


app.get('/', (req, res) => {
    res.send('Hello World');
});

app.post('/', (req, res) => {
    res.render('index', {
        title: 'Home',
        message: 'Welcome to the POST home page'
    });
});

// returns the rating of an input movie from IMDB
app.get('/m', (req, res) => {
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

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// app.use('/', router);

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});