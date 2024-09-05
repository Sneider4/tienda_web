from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
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
    dataP = Producto.query.all()
    dataC = Categoria.query.all()
    dataU = Usuario.query.all()
    total = 0

    if current_user.is_authenticated:
        dataCar = Carrito.query.filter_by(usuario_id=current_user.id).all()
    else:
        dataCar = []

    for item in dataCar:
        for producto in dataP:
            if producto.id == item.producto_id:
                total += producto.precio * item.cantidad

    impuesto = total * 0.19

    return render_template('producto/index.html', dataP=dataP, dataC=dataC, dataCar=dataCar, dataU=dataU, total=total, impuesto=impuesto)

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