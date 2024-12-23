from app import db

class Envio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)
    direccion_envio = db.Column(db.String(255), nullable=False)
    estado_envio = db.Column(db.String(50), default='Pendiente')
    fecha_envio = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'orden_id': self.orden_id,
            'direccion_envio': self.direccion_envio,
            'estado_envio': self.estado_envio,
            'fecha_envio': self.fecha_envio
            }
