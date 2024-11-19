from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.metodo_pago import MetodoPago
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('metodopagosocket', __name__, url_prefix='/Metodopagosockets')

@bp.route('/index', methods=['GET'])
def get_metodopago():
    metodospagos = MetodoPago.query.all()
    return jsonify([metodopago.to_dict() for metodopago in metodospagos]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_metodopago():
    data = request.json
    new_metodopago = MetodoPago(
        tipo = data['tipo'],
        numero_tarjeta = data['numero_tarjeta'],
        nombre_tarjeta = data['nombre_trajeta'],
        fecha_vencimiento = data['fecha_vencimiento'],
        codigo_seguridad = data['codigo_seguridad'])
    db.session.add(new_metodopago)
    db.session.commit()
    return jsonify({'message': 'Metodo de pago created successfully'}), 201


@bp.route('/update/<int:id>', methods=['PUT'])
def update_metodopago(id):
    metodopago = MetodoPago.query.get(id)
    if metodopago:
        data = request.json
        metodopago.tipo = data['tipo']
        metodopago.numero_tarjeta = data['numero_tarjeta']
        metodopago.nombre_tarjeta = data['nombre_trajeta']
        metodopago.fecha_vencimiento = data['fecha_vencimiento']
        metodopago.codigo_seguridad = data['codigo_seguridad']
        db.session.commit()
        return jsonify({'message': 'Metodo de pago updated successfully'})
    return jsonify({'message': ' Metodo de pago not found'}), 404

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_producto(id):
    metodopago = MetodoPago.query.get(id)
    if metodopago:
        db.session.delete(metodopago)
        db.session.commit()
        return jsonify({'message': 'Metodo de pago deleted successfully'})
    return jsonify({'message': 'Metodo de pago not found'}), 404


