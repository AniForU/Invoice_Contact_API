from src import app
from flask import request, jsonify
from src.data_model import AbnoramlChecking
from src.mongo_utility import mongo_utility
import statistics


@app.route("/checkAbnormalContactUri", methods=["POST"])
def get_abnormal_contact_info():
    try:
        request_body = request.get_json()
        try:
            transformed_request= AbnoramlChecking(**request_body)
            query = {
                "contact.organization": transformed_request.organization,
                "contact.name": {"$regex": ".*" + str(transformed_request.contactName) + ".*"}
            }
            colum_query = {"_id": 0,"amount.value":1}
            mongo = mongo_utility(app)
            result = mongo.get_documents(query,colum_query)
            #result = mytable.find(query, colum_query)
            if result.count==0:
                return_message = {
                    "Error":
                        {
                            "message": "No Data Found"
                        }
                }
                return jsonify(return_message), 404
            return calculate_abnoramlacy(transformed_request.amount,result)
        except Exception as e:
            return_message = {
                "Error":
                    {
                        "message": "Body content is not correct, please refer the documentation."
                    }
            }
            return jsonify(return_message), 404
    except:
        return "",404


def calculate_abnoramlacy(amount, result):
    different_amounts = []
    flag=True
    for x in result:
        flag = False
        different_amounts.append(x["amount"]["value"])
    if flag:
        return_message = {
            "Error":
                {
                    "message": "No Data Found"
                }
        }
        return return_message, 404
    mean_value = statistics.mean(different_amounts)
    standard_dev = statistics.pstdev(different_amounts)
    if amount >(mean_value+standard_dev) or amount<(mean_value-standard_dev):
        return_message={
            "abnormal":True
        }
        return return_message,200
    else:
        return_message={
            "abnormal":False
        }
        return return_message,200