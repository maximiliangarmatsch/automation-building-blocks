# API Documentation

## Form Submission

### Endpoint: `/submit_form`
- **Method:** POST
- **Description:** Submit a form with JSON data.
- **Request Body:**
  ```json
  {
    "key1": "value1",
    "key2": "value2"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Form submitted successfully",
    "data": {
      "key1": "value1",
      "key2": "value2"
    }
  }
  ```

## Product Inventory Management

### Endpoint: `/add_product`
- **Method:** POST
- **Description:** Add a new product to the inventory.
- **Request Body:**
  ```json
  {
    "name": "Coffee",
    "price": 10.99,
    "quantity": 100
  }
  ```
- **Response:**
  ```json
  {
    "message": "Product added successfully",
    "product": {
      "name": "Coffee",
      "price": 10.99,
      "quantity": 100
    }
  }
  ```

### Endpoint: `/get_products`
- **Method:** GET
- **Description:** Retrieve all products in the inventory.
- **Response:**
  ```json
  {
    "products": [
      {
        "name": "Coffee",
        "price": 10.99,
        "quantity": 100
      }
    ]
  }
  ```

### Endpoint: `/update_product/<product_id>`
- **Method:** PUT
- **Description:** Update an existing product in the inventory.
- **Request Body:**
  ```json
  {
    "name": "Espresso",
    "price": 12.99,
    "quantity": 80
  }
  ```
- **Response:**
  ```json
  {
    "message": "Product updated successfully",
    "product": {
      "name": "Espresso",
      "price": 12.99,
      "quantity": 80
    }
  }
  ```

### Endpoint: `/delete_product/<product_id>`
- **Method:** DELETE
- **Description:** Delete a product from the inventory.
- **Response:**
  ```json
  {
    "message": "Product deleted successfully",
    "product": {
      "name": "Coffee",
      "price": 10.99,
      "quantity": 100
    }
  }
  ```