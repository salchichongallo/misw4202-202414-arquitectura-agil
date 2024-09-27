from models import db, Usuario, UsuarioSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import request, jsonify

user_schema = UsuarioSchema()


class LoginController(Resource):

    def post(self):
        usuario = db.session.execute(
            db.select(Usuario).filter_by(
                correo=request.json["correo"],
                contrasena=request.json["contrasena"]
            )
        ).scalar()

        if usuario is None:
            return "Credenciales incorrectas", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


class RolController(Resource):
    @jwt_required()
    def get(self):
        usuario_id = get_jwt_identity()
        usuario = db.session.query(Usuario).get(usuario_id)
        response = {
            "rol": usuario.rol.value,
            "nombre": usuario.nombre
        }
        return response , 200
