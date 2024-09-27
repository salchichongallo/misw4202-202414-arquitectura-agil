from models import db, Usuario, RolEnum



# Insertar datos semilla
def insertar_datos_semilla():
    if Usuario.query.count() == 0:
        usuarios = [
            Usuario(nombre='Gerente1', correo='gerente1@example.com', contrasena='12345678', rol=RolEnum.GERENTE),
            Usuario(nombre='Cliente1', correo='cliente1@example.com', contrasena='12345678', rol=RolEnum.CLIENTE),
            Usuario(nombre='Agente1', correo='agente1@example.com', contrasena='12345678', rol=RolEnum.AGENTE),
            Usuario(nombre='Agente2', correo='agente2@example.com', contrasena='12345678', rol=RolEnum.AGENTE)
        ]
        db.session.bulk_save_objects(usuarios)
        db.session.commit()
        print("Datos semilla insertados.")
