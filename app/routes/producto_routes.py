from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, get_flashed_messages
from flask_login import current_user, login_required
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.carrito import Carrito
from app.models.direccion_cliente import DireccionCliente
from app import db
import os


bp = Blueprint('producto', __name__)

@bp.route('/producto')
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
@login_required
def add():
    rol = current_user.rol 
    if rol == "Administrador":
        if request.method == 'POST':
            try:
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

                new_producto = Producto(
                    nombre=nombre, 
                    precio=precio, 
                    descripcion=descripcion, 
                    stock=stock, 
                    categoria=categoria, 
                    imagen=filename
                )
                db.session.add(new_producto)
                db.session.commit()

                # Respuesta JSON indicando éxito
                return jsonify(success=True, message="Producto guardado con éxito")
            
            except Exception as e:
                # En caso de error, enviar el mensaje de error
                return jsonify(success=False, message=f"Ocurrió un error: {str(e)}")

        data = Categoria.query.all()
        return render_template('producto/add.html', data=data)
    
    else:
        return redirect(url_for('producto.index'))

@bp.route('/producto/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol != "Administrador":
        return redirect(url_for('producto.index'))

    dataP = Producto.query.get_or_404(id)
    dataC = Categoria.query.all()

    if request.method == 'POST':
        dataP.nombre = request.form['nombre']
        dataP.descripcion = request.form['descripcion']
        dataP.precio = request.form['precio']
        dataP.stock = request.form['stock']
        dataP.categoria_id = request.form['categoria']  # Cambiado a categoria_id si así está en tu modelo
        imagen = request.files['imagen']

        if imagen:
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static', 'images', filename)
            imagen.save(os.path.join(os.path.dirname(__file__), '..', imagen_path))
            dataP.imagen = filename

        db.session.commit()
        flash('Producto actualizado con éxito', 'success')
        return redirect(url_for('producto.tabla'))
    print(f"hola")

    return render_template('producto/edit.html', dataP=dataP, dataC=dataC)

@bp.route('/')
def ver_producto():

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

    return render_template('producto/ver_producto.html', dataP=dataP, dataC=dataC, dataCar=dataCar, dataU=dataU, total=total, impuesto=impuesto)

@bp.route('/producto/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    if current_user.rol == "Administrador":
        producto = Producto.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado con éxito', 'success')
        return redirect(url_for('producto.tabla'))
    else:
        return redirect(url_for('producto.index'))
    
@bp.route('/tabla')
@login_required
def tabla():
    dataP = Producto.query.all()
    dataC = Categoria.query.all()
    return render_template('producto/tabla.html', dataP=dataP, dataC=dataC)