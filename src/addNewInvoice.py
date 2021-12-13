from src import app
from flask import request, jsonify
from src.data_model import Invoice
from src.mongo_utility import mongo_utility
from utility import JsonConverter
from pymongo.errors import WriteError

@app.route("/addInvoice", methods=["POST"])
def add_new_invoice():
    """Adding new invoice to the database"""
    invoice_data = request.get_json()
    try:
        #to check the body is matching and its datatypes
        invoice = Invoice(**invoice_data)
        try:
            mongo = mongo_utility(app)
            result = mongo.insert_document(invoice_data)
            return JsonConverter.JsonConverter().encode(result.inserted_id),201
        except WriteError as e:
            return_message = {
                "Error":
                    {
                        "message": "Duplicate Id Occured"
                    }
            }
            return jsonify(return_message), 205
        except Exception as e:

            return_message = {
                "Error":
                    {
                        "message": "Body content is not correct, please refer the documentation."
                    }
            }
        return jsonify(return_message), 400

    except Exception as e:
        return_message = {
            "Error":
                {
                    "message": "Body content is not correct, please refer the documentation."
                }
        }
        return jsonify(return_message), 400
