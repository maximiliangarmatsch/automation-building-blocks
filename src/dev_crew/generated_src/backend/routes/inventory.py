# routes/inventory.py

from flask import Blueprint, request, jsonify

bp = Blueprint('inventory', __name__)

# In-memory product inventory
inventory = []

@bp.route('/add_product', methods=['POST'])
def add_product():
    product = request.get_json()
    inventory.append(product)
    return jsonify({'message': 'Product added successfully', 'product': product})

@bp.route('/get_products', methods=['GET'])
def get_products():
    return jsonify({'products': inventory})

@bp.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    updated_product = request.get_json()
    if 0 <= product_id < len(inventory):
        inventory[product_id] = updated_product
        return jsonify({'message': 'Product updated successfully', 'product': updated_product})
    else:
        return jsonify({'message': 'Product not found'}), 404

@bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 0 <= product_id < len(inventory):
        deleted_product = inventory.pop(product_id)
        return jsonify({'message': 'Product deleted successfully', 'product': deleted_product})
    else:
        return jsonify({'message': 'Product not found'}), 404