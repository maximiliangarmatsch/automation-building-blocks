# app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# Import routes
from routes import form, inventory

# Register Blueprints
app.register_blueprint(form.bp)
app.register_blueprint(inventory.bp)

if __name__ == '__main__':
    app.run(debug=True)