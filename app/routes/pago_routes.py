from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.pago import Pago
from app import db

bp = Blueprint('pago', __name__)

@bp.route('/pago')
def index():
    data = Pago.query.all()
    return render_template('pago/index.html', data=data)