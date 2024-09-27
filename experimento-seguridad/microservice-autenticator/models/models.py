from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum


db = SQLAlchemy()

class RolEnum(enum.Enum):
    GERENTE = "GERENTE"
    CLIENTE = "CLIENTE"
    AGENTE = "AGENTE"


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)
    rol = db.Column(Enum(RolEnum), nullable=False)
    permisos = db.Column(db.String(50), nullable=False)

    def set_permisos(self, permisos_list):
        self.permisos = ','.join(permisos_list)

    def get_permisos(self):
        return self.permisos.split(',')

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True

