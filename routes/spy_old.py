# import json
# import logging

# from flask import request
# from routes import app

# logger = logging.getLogger(__name__)


# @app.route('/investigate', methods=['POST'])
# def investigate_evaluate():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     input_value = data.get("input")
#     result = input_value * input_value
#     logging.info("My result :{}".format(result))
#     return json.dumps(result)
