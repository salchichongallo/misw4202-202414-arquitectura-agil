import requests
from flask import request, jsonify
from flask_restful import Resource

class AuthController(Resource):
    def post(self):
        # Recibe las credenciales del cliente
        data = request.get_json()

        # Envia las credenciales al microservicio de autenticación
        response = requests.post('http://localhost:5001/login', json=data)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'message': 'Credenciales incorrectas'}), response.status_code
