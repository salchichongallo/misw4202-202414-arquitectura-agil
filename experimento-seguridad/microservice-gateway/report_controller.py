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

        if response.status_code == 200:
            # Devolver la respuesta JSON directamente
            return make_response(response.json(), 200)
        else:
            return make_response({'message': 'Error al obtener el reporte'}, response.status_code)
