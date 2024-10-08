from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.carrito import Carrito
from app.models.direccion_cliente import DireccionCliente
from app.models.metodo_pago import MetodoPago
from app import db

bp = Blueprint('pago', __name__)

@bp.route('/pago/shopping')
def shopping():
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

    return render_template('pago/shopping.html', dataP=dataP, dataC=dataC, dataCar=dataCar, dataU=dataU, total=total, impuesto=impuesto)

@bp.route('/pago/identificacion')
def identificacion():
    dataP = Producto.query.all()
    dataC = Categoria.query.all()
    dataU = Usuario.query.all()
    total = 0

    usuario_id = current_user.id
    direccion_cliente = DireccionCliente.query.filter_by(usuario_id=usuario_id).first()
    metodo_pago = MetodoPago.query.filter_by(usuario_id=usuario_id).first()

    if current_user.is_authenticated:
        dataCar = Carrito.query.filter_by(usuario_id=current_user.id).all()
    else:
        dataCar = []

    for item in dataCar:
        for producto in dataP:
            if producto.id == item.producto_id:
                total += producto.precio * item.cantidad

    impuesto = total * 0.19

    return render_template('pago/identificacion.html', direccion_cliente=direccion_cliente, dataP=dataP, dataC=dataC, dataCar=dataCar, dataU=dataU, total=total, impuesto=impuesto, metodo_pago=metodo_pago)