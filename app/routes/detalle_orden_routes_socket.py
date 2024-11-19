from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.detalle_orden import DetalleOrden
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('detalleordensocket', __name__, url_prefix='/Detalleordensockets')

@bp.route('/index', methods=['GET'])
def get_detalleorden():
    detallesordenes = DetalleOrden.query.all()
    return jsonify([detalleorden.to_dict() for detalleorden in detallesordenes]), 200, {'content-Type': 'application/json'}
