import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class ReportController(Resource):
    @jwt_required()
    def get(self, report_id):
        # Obtener el token JWT del usuario
        token = request.headers.get('Authorization')

        # Reenviar la solicitud al microservicio de reportes
        headers = {'Authorization': token}
        response = requests.get(f'http://localhost:5002/reports/{report_id}', headers=headers)

        return make_response(response.json(), response.status_code)
