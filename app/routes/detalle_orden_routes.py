from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.detalle_orden import DetalleOrden
from app import db

bp = Blueprint('detalle_orden', __name__)

@bp.route('/detalle_orden')
def index():
    data = DetalleOrden.query.all()
    return render_template('detalle_orden/index.html', data=data)

@bp.route('/detalle_orden/<int:orden_id>')
def detalle_orden(orden_id):
    data = DetalleOrden.query.filter_by(orden_id=orden_id).all()
    return render_template('pago/factura.html', data=data)