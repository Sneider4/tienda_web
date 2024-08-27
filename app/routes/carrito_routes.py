from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.carrito import Carrito
from app import db

bp = Blueprint('carrito', __name__)

@bp.route('/carrito')
def index():
    data = Carrito.query.all()
    return render_template('carrito/index.html', data=data)