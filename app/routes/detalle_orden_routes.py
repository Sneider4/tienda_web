from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.detalle_orden import DetalleOrden
from app import db

bp = Blueprint('detalle_orden', __name__)

@bp.route('/detalle_orden')
def index():
    data = DetalleOrden.query.all()
    return render_template('detalle_orden/index.html', data=data)