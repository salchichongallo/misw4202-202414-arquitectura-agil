from api_gateway import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

class VistaLlamadas(Resource):
    def post(self):
        monitor_ms = "http://127.0.0.1:5001/assign-call"
        content = requests.post(monitor_ms, json=request.json)
        response = content.json()
        return response


api.add_resource(VistaLlamadas, '/call')
