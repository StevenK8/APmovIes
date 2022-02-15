








const express = require("express");
const controllers = require("./api");
const config = require("./config/config");
//Add swagger
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');
const swaggerJSDoc = require('swagger-jsdoc');
const getMovieDocs = require('./docs/getMovie.js') 

async function startServer() {
  const app = express();

  await require("./loaders")(app);

  
const swaggerDefinition = {
  openapi: '3.0.0',
  info: {
    title: 'Movie API',
    version: '1.0.0',
  },
  paths: {
    '/movie': {
      getMovieDocs
    }
  }
};

const options = {
  swaggerDefinition,
  // Paths to files containing OpenAPI definitions
  apis: ['./routes/*.js'],
};

const swaggerSpec = swaggerJSDoc(options);
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

  app.listen(config.port, (err) => {
    if (err) {
      Logger.error(err);
      process.exit(1);
      return;
    }
    console.log(`
        ################################################
        🛡️  Server listening on port: ${config.port} 🛡️ 
        ################################################
      `);
  });
}

startServer();
