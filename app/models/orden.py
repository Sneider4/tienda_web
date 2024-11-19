from app import db

class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_orden = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.Float, nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey('direccion_cliente.id'), nullable=False)  
    metodo_pago = db.Column(db.String(50), nullable=False)
    
    direccion = db.relationship('DireccionCliente', backref='orden')
    detalles = db.relationship('DetalleOrden', back_populates='orden')
    usuario = db.relationship('Usuario', backref='ordenes') 

    def to_dict(self):
        return{
            "id": self.id,
            "usuario_id": self.usuario_id,
            "fecha_orden": self.fecha_orden,
            "total": self.total,
            "direccion_id": self.direccion_id,
            "metodo_pago": self.metodo_pago,
<<<<<<< Updated upstream
        }
=======
            
        }
    
>>>>>>> Stashed changes
