from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.orden import Orden
from app import db

bp = Blueprint('orden', __name__)

@bp.route('/orden')
def index():
    data = Orden.query.all()
    return render_template('orden/index.html', data=data)