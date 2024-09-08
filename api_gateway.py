from api_gateway import create_app
from flask_restful import Resource, Api
from flask import request
import requests
import time
from datetime import datetime
import os

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

file_name = "calls_response.txt"
file_path = os.path.join("responses", file_name)
counter = 0

def create_file():
    try:
        os.remove("responses/calls_response.txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except OSError:
        pass

class VistaLlamadas(Resource):
    create_file()

    def post(self):
        global counter
        counter += 1
        start_time = time.time()
        monitor_ms = "http://127.0.0.1:5001/assign-call"
        requests.post(monitor_ms, json=request.json)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        response = {
            "call_number": counter,
            "call_date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "response_time": f"{response_time} ms"
        }

        with open(file_path, "a") as file:
            file.write(str(response) + "\n")

        return response


api.add_resource(VistaLlamadas, '/call')
