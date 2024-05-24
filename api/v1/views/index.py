#!/usr/bin/python3
""" new view for api route """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
