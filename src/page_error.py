from src import app
from flask import jsonify

@app.errorhandler(404)
def page_not_found(e):
    """Generic Message to user for 404"""
    # Message to the user
    return_message = {
        "Error":
            {
                "message": "This uri is not supported, Please refer API document."
            }
    }
    # Making the message looks good
    resp = jsonify(return_message)
    # Sending response
    resp.status_code = 404
    # Returning the object
    return resp