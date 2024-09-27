from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from auth_controller import AuthController
from report_controller import ReportController


app = Flask(__name__)

# Configura la clave secreta para JWT
app.config['JWT_SECRET_KEY'] = 'frase-secreta' 
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
jwt = JWTManager(app)


api.add_resource(AuthController, '/auth/login')
api.add_resource(ReportController, '/gateway/reports/<int:report_id>')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
