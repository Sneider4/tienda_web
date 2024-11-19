from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.orden import Orden
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('ordensocket', __name__, url_prefix='/Ordensockets')

@bp.route('/index', methods=['GET'])
<<<<<<< Updated upstream
def get_user():
    ordenes = Orden.query.all()
    return jsonify([orden.to_dict() for orden in ordenes]), 200, {'content-Type': 'application/json'}
=======
def get_orden():
    ordenes = Orden.query.all()
    return jsonify([orden.to_dict() for orden in ordenes]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_orden():
    data = request.json
    new_orden = Orden(
        usuario_id = data['usuario_id'],
        fecha_orden = data['fecha_orden'],
        total = data['total'],
        direccion_id = data['direccion_id'],
        metodo_pago = data['metodo_pago'])
    db.session.add(new_orden)
    db.session.commit()
    return jsonify({'message': 'Orden created successfully'}), 201


@bp.route('/update/<int:id>', methods=['PUT'])
def update_orden(id):
    orden = Orden.query.get(id)
    if orden:
        data = request.json
        orden.usuario_id = data['usuario_id']
        orden.fecha_orden = data['fecha_orden']
        orden.total = data['total']
        orden.direccion_id = data['direccion_id']
        orden.metodo_pago = data['metodo_pago']
        db.session.commit()
        return jsonify({'message': 'Orden updated successfully'})
    return jsonify({'message': ' Orden not found'}), 404

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_producto(id):
    orden = Orden.query.get(id)
    if orden:
        db.session.delete(orden)
        db.session.commit()
        return jsonify({'message': 'Orden deleted successfully'})
    return jsonify({'message': 'Orden not found'}), 404


>>>>>>> Stashed changes
