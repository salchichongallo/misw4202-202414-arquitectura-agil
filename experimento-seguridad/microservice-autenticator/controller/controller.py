from models import db, Usuario, UsuarioSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import request, jsonify

user_schema = UsuarioSchema()


class LoginController(Resource):
    def post(self):
        # Buscar el usuario por el correo
        usuario = db.session.execute(
            db.select(Usuario).filter_by(
                correo=request.json["correo"]
            )
        ).scalar()

        # Validar si el usuario existe
        if usuario is None:
            return {"mensaje": "Usuario no encontrado"}, 404

        # Validar la contraseña
        if usuario.contrasena != request.json["contrasena"]:
            return {"mensaje": "Credenciales incorrectas"}, 400

        # Si el usuario existe y la contraseña es correcta, generar el token
        token_de_acceso = create_access_token(identity=usuario.id)
        return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}, 200



class RolController(Resource):
    @jwt_required()
    def get(self):
        usuario_id = get_jwt_identity()
        usuario = db.session.query(Usuario).get(usuario_id)

        # Obtener el permiso del query param
        permiso_requerido = request.args.get('permiso')

        # Validar si el permiso fue pasado en los query params
        if permiso_requerido is None:
            return {"mensaje": "Permiso no especificado"}, 400

        # Obtener los permisos del usuario como una lista
        permisos_usuario = usuario.get_permisos()
        # Validar si el usuario tiene el permiso requerido
        if permiso_requerido not in permisos_usuario:
            return {"mensaje": "Acceso denegado: Permiso insuficiente"}, 403

        response = {
            "rol": usuario.rol.value,
            "nombre": usuario.nombre,
            "permisos": permisos_usuario
        }
        return response , 200
