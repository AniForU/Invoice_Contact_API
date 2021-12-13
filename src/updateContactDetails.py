from src import app
from flask import request, jsonify
from src.data_model import Contact
from src.mongo_utility import mongo_utility


@app.route("/updateContact", methods=["POST"])
def update_contact_details():
    contact_data = request.get_json()
    try:
        contact = Contact(**contact_data)
    except Exception as e:
        return_message = {
            "Error":
                {
                    "message": "Body content is not correct, please refer the documentation."
                }
        }
        return jsonify(return_message), 404

    try:
        contact_id = contact.id
        update_query = {"contact._id": contact_id}
        update_value = {"$set": {"contact": contact_data}}
        mongo = mongo_utility(app)
        status = mongo.update_documents(update_query, update_value)
        message = "Invoices updated " + str(status.modified_count)
        return_message = {
            "message": message
        }
        return jsonify(return_message), 200
    except:
        return "", 400