from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.envio import Envio
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('enviosocket', __name__, url_prefix='/Enviosockets')

@bp.route('/index', methods=['GET'])
def get_envio():
    envios = Envio.query.all()
    return jsonify([envio.to_dict() for envio in envios]), 200, {'content-Type': 'application/json'}
