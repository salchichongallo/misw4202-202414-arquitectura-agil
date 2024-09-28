import requests
from flask import request, jsonify
from flask_restful import Resource

class AuthController(Resource):
    def post(self):
        # Recibe las credenciales del cliente
        data = request.get_json()

        # Envía las credenciales al microservicio de autenticación
        try:
            response = requests.post('http://localhost:5001/login', json=data)

            return response.json(), response.status_code

        except requests.exceptions.RequestException as e:
            # En caso de error de conexión u otro tipo de error en la solicitud
            return {'message': f'Error al conectar con el servicio de autenticación: {str(e)}'}, 500
