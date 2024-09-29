from app import db

class MetodoPago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    numero_tarjeta = db.Column(db.String(20), nullable=False)
    nombre_tarjeta = db.Column(db.String(100), nullable=False)
    fecha_vencimiento = db.Column(db.String(10), nullable=False)
    codigo_seguridad = db.Column(db.String(4), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)