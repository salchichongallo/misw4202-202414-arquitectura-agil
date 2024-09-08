from api_gateway import create_app
from flask_restful import Resource, Api
from flask import Flask, request

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

class VistaLlamadas(Resource):
    def post(self):
        return { 'data': request.json }

api.add_resource(VistaLlamadas, '/call')
