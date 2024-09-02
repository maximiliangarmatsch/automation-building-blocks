# API Documentation

## Base URL
```
http://localhost:3000/api
```

## Endpoints

### Submit Form

**Endpoint:** `/submit`

**Method:** `POST`

**Description:** This endpoint handles form submissions and saves the data to a JSON file.

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "message": "string"
}
```

**Response:**
```json
{
  "message": "Form submitted successfully!"
}

**Status Codes:**
- `201`: Form submission was successful.
- `400`: Bad request. The request body is invalid.
```