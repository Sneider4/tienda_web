from flask_login import UserMixin
from app import db

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    contrasena = db.Column(db.String(120), nullable=False)
    departamento = db.Column(db.String(255))
    ciudad = db.Column(db.String(255))
    genero = db.Column(db.String(255))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    rol = db.Column(db.String(50), default='Cliente')