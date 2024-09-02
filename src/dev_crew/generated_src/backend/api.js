// api.js
const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();
const dataFilePath = path.join(__dirname, 'data.json');

// Helper function to read data from the JSON file
function readData() {
  const data = fs.readFileSync(dataFilePath);
  return JSON.parse(data);
}

// Helper function to write data to the JSON file
function writeData(data) {
  fs.writeFileSync(dataFilePath, JSON.stringify(data, null, 2));
}

// Endpoint to handle form submissions
router.post('/submit', (req, res) => {
  const formData = req.body;
  const data = readData();
  data.submissions.push(formData);
  writeData(data);
  res.status(201).send({ message: 'Form submitted successfully!' });
});

module.exports = router;