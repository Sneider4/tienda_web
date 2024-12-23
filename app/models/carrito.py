from app import db

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    usuario = db.relationship('Usuario', backref='carritos')

    def to_dict(self):
        return{
            "id": self.id,
            "usuario_id": self.usuario_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
        }
        