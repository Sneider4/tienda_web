from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    detalles_orden = db.relationship('DetalleOrden', back_populates='producto')    

    def to_dict(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria,
            "imagen": self.imagen
        }
        