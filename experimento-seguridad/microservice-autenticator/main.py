from models import db
from flask import Flask
from utils.utils import insertar_datos_semilla
from flask_jwt_extended import JWTManager
from flask_restful import Api
from controller.controller import LoginController, RolController

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

insertar_datos_semilla()

api = Api(app)
api.add_resource(LoginController, '/login')
api.add_resource(RolController, '/validate-rol')

jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(debug=False, port=5001)
