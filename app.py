"""
Rubix Coding Challenge - Rubix Bakery

The Rubix Bakery Order processing system
is developed as an API that accepts
orders in json format.

Each request received may contain multiple orders

Response is sent as json

Author: Renji Harold <renjiharold@nbnco.com.au>
Started: 28 October 2018.
"""
from flask import Flask, jsonify, request

from bakery.bakery import process_orders
from bakery.products import BakeryProducts

app = Flask(__name__)

app.config.update(DEBUG=True, JSONIFY_PRETTYPRINT_REGULAR=True)


@app.route("/")
def index():
    return jsonify(BakeryProducts.SAMPLE_ORDER)


@app.route("/order", methods=["POST", "GET"])
def compute_order():
    if request.method == "GET":
        return jsonify(BakeryProducts.SAMPLE_ORDER)
    else:
        if request.data and request.json.get("order"):
            return jsonify(process_orders(request.json.get("order")))
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Please provider order in proper format",
                    }
                ),
                400,
            )
