// server.js
const express = require('express');
const app = express();
const api = require('./api');
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use('/api', api);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});