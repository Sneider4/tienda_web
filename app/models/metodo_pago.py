from app import db

class MetodoPago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    numero_tarjeta = db.Column(db.String(20), nullable=False)
    nombre_tarjeta = db.Column(db.String(100), nullable=False)
    fecha_vencimiento = db.Column(db.String(10), nullable=False)
    codigo_seguridad = db.Column(db.String(4), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "tipo": self.tipo,
            "numero_tarjeta": self.numero_tarjeta,
            "nombre_tarjeta": self.nombre_tarjeta,
            "fecha_vencimiento": self.fecha_vencimiento,
            "codigo_seguridad": self.codigo_seguridad
        }
        