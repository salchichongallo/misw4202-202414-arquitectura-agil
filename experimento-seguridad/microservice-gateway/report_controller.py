import requests
from flask import request, jsonify
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
            return jsonify(response.json())
        else:
            return jsonify({'message': 'Error al obtener el reporte'}), response.status_code
