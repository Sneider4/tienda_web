from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.carrito import Carrito
from app.models.direccion_cliente import DireccionCliente
from app import db
import os, app


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

from flask import flash, redirect, url_for

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

                 # Mensaje flash indicando éxito
                flash("Producto guardado con éxito", "success")
                return redirect(url_for('producto.tabla'))  # Redirige a la lista de productos o a la página adecuada
            
            except Exception as e:
                # Mensaje flash indicando error
                flash(f"Ocurrió un error: {str(e)}", "danger")
                return redirect(url_for('producto.add'))  # Redirige nuevamente al formulario para intentar de nuevo


        data = Categoria.query.all()
        return render_template('producto/add.html', data=data)
    
    else:
        return redirect(url_for('administrador.index'))


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
        dataP.categoria = request.form['categoria']  # Cambiado a id si así está en tu modelo
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

@bp.route('/producto/ver_producto/<int:id>', methods = ['GET'])
def ver_producto(id):

    dataP = Producto.query.get_or_404(id)
    dataC = Categoria.query.all()
    dataU = Usuario.query.all()
    total = 0

    
    return render_template('producto/ver_producto.html', dataP=dataP, dataC=dataC, dataU=dataU, total=total)

@bp.route('/producto/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:    
        if current_user.rol == "Administrador":
            producto = Producto.query.get_or_404(id)
            db.session.delete(producto)
            db.session.commit()
            flash('Producto eliminado con éxito', 'success')
            return redirect(url_for('producto.tabla'))
        else:
            return redirect(url_for('producto.index'))
    except:
        flash('El producto no se puede eliminar porque se está usando el registro en otras tablas', 'danger')
        return redirect(url_for('producto.tabla'))

@bp.route('/tabla')
@login_required
def tabla():

    if current_user.rol == "Administrador":
        dataP = Producto.query.all()
        dataC = Categoria.query.all()
        return render_template('producto/tabla.html', dataP=dataP, dataC=dataC)
    else:
        return redirect(url_for('producto.index'))

@bp.route('/inventario')
@login_required
def inventario():
    if current_user.rol == "Administrador":
        # Obtener todos los productos con sus categorías
        productos = db.session.query(Producto, Categoria).join(Categoria, Producto.categoria == Categoria.id).all()
        
        # Calcular el valor total del inventario
        valor_total_inventario = sum(producto.precio * producto.stock for producto, _ in productos)
        
        # Obtener estadísticas
        total_productos = len(productos)
        productos_sin_stock = sum(1 for producto, _ in productos if producto.stock == 0)
        
        # Preparar los datos para la plantilla
        productos_data = []
        for producto, categoria in productos:
            productos_data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'stock': producto.stock,
                'categoria': categoria.nombre  # Asumiendo que la categoría tiene un atributo 'nombre'
            })
        
        return render_template('inventario/index.html', 
                               productos=productos_data, 
                               valor_total_inventario=valor_total_inventario,
                               total_productos=total_productos,
                               productos_sin_stock=productos_sin_stock)
    else:
        flash('No tienes permiso para acceder al inventario', 'danger')
        return redirect(url_for('producto.index'))

