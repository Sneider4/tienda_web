from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.carrito import Carrito
from app import db
import os

bp = Blueprint('producto', __name__)

@bp.route('/')
def index():
    data = Producto.query.all()
    dataC = Categoria.query.all()
    dataU = Usuario.query.all()
    dataCar = Carrito.query.all()

    return render_template('producto/index.html', data=data, dataC=dataC, dataCar=dataCar, dataU=dataU)

@bp.route('/producto/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        categoria = request.form['categoria']
        imagen = request.files['imagen'] 

        if imagen:
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static', 'images', filename)
            imagen.save(os.path.join(os.path.dirname(__file__), '..', imagen_path))
            ruta_imagen = imagen_path

        else:
            ruta_imagen = None
        
        new_producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion, stock=stock, categoria=categoria, imagen=imagen.filename)
        db.session.add(new_producto)
        db.session.commit()
        
        return redirect(url_for('producto.index'))

    data = Categoria.query.all()
    return render_template('producto/add.html', data=data)