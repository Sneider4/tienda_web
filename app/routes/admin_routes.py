from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.carrito import Carrito
from app.models.orden import Orden

from app import db
import os


bp = Blueprint('admin', __name__)

@bp.route('/admin')
def index():
    dataP = Producto.query.all()
    dataC = Categoria.query.all()
    dataU = Usuario.query.all()
    tamañoU = len(dataU)
    ordenes = Orden.query.all()
    tamañoO = len(ordenes)
    total = 0
    usuario = current_user

    if current_user.is_authenticated:
        dataCar = Carrito.query.filter_by(usuario_id=current_user.id).all()
    else:
        dataCar = []

    for item in dataCar:
        for producto in dataP:
            if producto.id == item.producto_id:
                total += producto.precio * item.cantidad

    impuesto = total * 0.19

    return render_template('administrador/index.html', dataP=dataP, dataC=dataC, dataCar=dataCar, dataU=dataU, total=total, impuesto=impuesto, tamañoU=tamañoU, ordenes=ordenes, usuario=usuario, tamañoO=tamañoO)



@bp.route('/admin/layout_sidenav_light')
def layout_sidenav_light():
    return render_template('admin/layout-sidenav-light.html')

@bp.route('/admin/tables')
def tables():
    dataP = Producto.query.all()
    dataC = Categoria.query.all()

    return render_template('admin/tables.html', dataP=dataP,dataC=dataC)

@bp.route('/admin/charts')
def charts():
    return render_template('admin/charts.html')

    
@bp.route('/producto/tabla')
def tabla():
    dataP = Producto.query.all()
    dataC = Categoria.query.all()
    usuario = current_user

    return render_template('producto/tabla.html', dataP=dataP,dataC=dataC, usuario=usuario)

@bp.route('/admin/clientes')
def clientes():
    dataU = Usuario.query.all()
    usuario = current_user

    return render_template('administrador/clientes.html', dataU=dataU, usuario=usuario)


@bp.route('/admin/configuracion')
def configuracion():
    dataU = Usuario.query.all()
    usuario = current_user

    return render_template('administrador/configuraciones.html', dataU=dataU, usuario=usuario)


@bp.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_imagen(id):

    dataU = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        imagen = request.files['imagen']

        if imagen:
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static', 'images', filename)
            imagen.save(os.path.join(os.path.dirname(__file__), '..', imagen_path))
            dataU.imagen = filename

        db.session.commit()
        flash('Imagen actualizada con éxito', 'success')
        return redirect(url_for('admin.index'))