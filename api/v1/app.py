#!/usr/bin/python3
""" flask app for api route """


from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exception):
    """ close the connection """
    storage.close()


@app.errorhandler(404)
def nop(error):
    """ route for 404 """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def nop2(error):
    """ route for 400 """
    error_msg = error.description
    return error_msg, 400


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
