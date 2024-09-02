from flask import request, jsonify

# In-memory database for demonstration purposes
products = []
form_submissions = []

def setup_routes(app):
    @app.route('/api/form-submit', methods=['POST'])
    def form_submit():
        data = request.json
        form_submissions.append(data)
        return jsonify({'message': 'Form submitted successfully'}), 201

    @app.route('/api/products', methods=['GET', 'POST'])
    def manage_products():
        if request.method == 'POST':
            data = request.json
            products.append(data)
            return jsonify({'message': 'Product added successfully'}), 201
        elif request.method == 'GET':
            return jsonify(products), 200

    @app.route('/api/products/<int:product_id>', methods=['PUT', 'DELETE'])
    def update_delete_product(product_id):
        if request.method == 'PUT':
            data = request.json
            for product in products:
                if product['id'] == product_id:
                    product.update(data)
                    return jsonify({'message': 'Product updated successfully'}), 200
            return jsonify({'message': 'Product not found'}), 404

        elif request.method == 'DELETE':
            global products
            products = [product for product in products if product['id'] != product_id]
            return jsonify({'message': 'Product deleted successfully'}), 200