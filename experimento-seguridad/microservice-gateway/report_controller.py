import requests
from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class ReportController(Resource):
    @jwt_required()
    def get(self, report_id):
        response = requests.get(f'http://127.0.0.1:5002/reports/{report_id}', headers=request.headers)
        return make_response(response.json(), response.status_code)
