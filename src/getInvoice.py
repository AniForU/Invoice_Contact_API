from src import app
from flask import request, jsonify
from src.mongo_utility import mongo_utility


@app.route("/invoice/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    """Getting Invoice from the database"""
    mongo = mongo_utility(app)

    invoice_data = mongo.get_document({"_id": str(invoice_id)})
    if invoice_data is None:
        return jsonify({'message':'No data found'}),200
    return jsonify(invoice_data), 200

