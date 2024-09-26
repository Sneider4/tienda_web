from app import db

class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_orden = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')
    direccion_id = db.Column(db.Integer, db.ForeignKey('direccion_cliente.id'), nullable=False)  
    
    direccion = db.relationship('DireccionCliente', backref='orden')
    productos = db.relationship('DetalleOrden', backref='orden', lazy=True)