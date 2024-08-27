from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.envio import Envio
from app import db

bp = Blueprint('envio', __name__)

@bp.route('/envio')
def index():
    data = Envio.query.all()
    return render_template('envio/index.html', data=data)