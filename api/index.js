const express = require('express');
const imdb = require('./routes/imdb');
const router = express.Router();

module.exports = () => {
    router.use('/imdb',imdb());

    return router;
};
// const express = require('express');
// // const router = express.Router();
// const app = express();
// // Add swagger
// const swaggerUi = require('swagger-ui-express');
// // const swaggerDocument = require('./swagger.json');
// const swaggerJSDoc = require('swagger-jsdoc');


// app.get('/', (req, res) => {
//     res.send('Hello World');
// });

// app.post('/', (req, res) => {
//     res.render('index', {
//         title: 'Home',
//         message: 'Welcome to the POST home page'
//     });
// });

// // returns the rating of an input movie from IMDB
// app.get('/m', (req, res) => {
//     req = req.query;
//     var movie = req.movie;
//     var url = 'http://www.omdbapi.com/?t=' + movie + '&apikey=thewdb';
//     var request = require('request');
//     request(url, function (error, response, body) {
//         if (!error && response.statusCode == 200) {
//             var json = JSON.parse(body);
//             var rating = json.imdbRating;
//             res.send(rating);
//         }
//     });
// });

// // app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// const swaggerDefinition = {
//   openapi: '3.0.0',
//   info: {
//     title: 'Movie API',
//     version: '1.0.0',
//   },
// };

// const options = {
//   swaggerDefinition,
//   // Paths to files containing OpenAPI definitions
//   apis: ['./routes/*.js'],
// };

// const swaggerSpec = swaggerJSDoc(options);

// app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// // app.use('/', router);

// app.listen(3000, () => {
//     console.log('Server is running on port 3000');
// });