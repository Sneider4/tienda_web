from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db
from flask import current_app

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


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)