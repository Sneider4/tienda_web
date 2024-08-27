from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)