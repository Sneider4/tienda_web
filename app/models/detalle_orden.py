from app import db

class DetalleOrden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    orden = db.relationship('Orden', back_populates='detalles')
    producto = db.relationship('Producto', back_populates='detalles_orden')

    def to_dict(self):
        return {
            "id": self.id,
            "orden_id": self.orden_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio": self.precio
            }