from src import app
from flask import request, jsonify
from src.data_model import SuggestInvoice
from src.mongo_utility import mongo_utility


@app.route("/suggestContactInvoice", methods=["POST"])
def get_match_suggest_contact():
    request_body = request.get_json()
    try:
        contact = SuggestInvoice(**request_body)
        query = {
            "contact.organization": contact.organization,
            "contact.name": {"$regex": ".*" + str(contact.contactName) + ".*"}
        }
        column_query = {"_id": 0, "contact.name": 1}
        try:
            mongo = mongo_utility(app)
            result = mongo.get_documents(query, column_query)
            total_score = result.count()
            if total_score==0:
                return_message = {
                    "Error":
                        {
                            "message": "No Data Found"
                        }
                }
                return jsonify(return_message), 205
            response= check_confidence_contact(result,total_score)
            return jsonify(response[0]), response[1]
        except:
            if result.count() <= 0:
                message = {
                    "Message": "Could not get any result"
                }
            return jsonify(message), 205

    except Exception as e:
        return_message = {
            "Error":
                {
                    "message": "Body content is not correct, please refer the documentation."
                }
        }
        return jsonify(return_message), 400


def check_confidence_contact(result,total_score):
    nameCount = dict()
    for x in result:
        word = x["contact"]["name"]
        if word in nameCount:
            nameCount[word] += 1
        else:
            nameCount[word] = 1
    max = 0
    output_name = ""
    for name, count in nameCount.items():
        if count > max:
            max = count
            output_name = name
    score = max / total_score
    returnMatchPercent = "{:.2f}".format(score)
    response = {
        "suggestedContact": output_name,
        "confidence": float(returnMatchPercent)
    }
    return response,200
