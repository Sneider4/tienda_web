from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.orden import Orden
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('ordensocket', __name__, url_prefix='/Ordensockets')

@bp.route('/index', methods=['GET'])
def get_user():
    ordenes = Orden.query.all()
    return jsonify([orden.to_dict() for orden in ordenes]), 200, {'content-Type': 'application/json'}