from app import db

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    fecha_pago = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado_pago = db.Column(db.String(50), default='Pendiente')