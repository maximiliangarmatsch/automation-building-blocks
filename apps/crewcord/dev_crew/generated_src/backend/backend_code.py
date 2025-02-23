from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/products", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to our ecommerce API"})


if __name__ == "__main__":
    app.run(debug=True)
