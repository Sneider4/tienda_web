from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.carrito import Carrito
from app import db
import os


bp = Blueprint('admin', __name__)

@bp.route('/admin')
def index():
    dataP = Producto.query.all()
    dataC = Categoria.query.all()
    dataU = Usuario.query.all()
    tamaño = len(dataU)
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

    return render_template('administrador/index.html', dataP=dataP, dataC=dataC, dataCar=dataCar, dataU=dataU, total=total, impuesto=impuesto, tamaño=tamaño)


@bp.route('/admin/layout_static')
def layout_static():
    
    dataC = Categoria.query.all()
    
    return render_template('categoria/layout-static.html',  dataC=dataC)

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

    return render_template('producto/tabla.html', dataP=dataP,dataC=dataC)

@bp.route('/admin/clientes')
def clientes():
    dataU = Usuario.query.all()

    return render_template('administrador/clientes.html', dataU=dataU)