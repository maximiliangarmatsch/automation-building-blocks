const express = require('express');
const apiRouter = require('./routes/api');

const app = express();
app.use(express.json());

app.use('/api', apiRouter);

app.get('/', (req, res) => {
  res.send('Welcome to the AI Software Agency Backend!');
});

module.exports = app;