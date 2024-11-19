from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.direccion_cliente import DireccionCliente
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('direccionclientesocket', __name__, url_prefix='/Direccionclientesockets')

@bp.route('/index', methods=['GET'])
def get_direccioncliente():
    direccionclinetes = DireccionCliente.query.all()
    return jsonify([direccioncliente.to_dict() for direccioncliente in direccionclinetes]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_metodopago():
    data = request.json
    new_direccioncliente = DireccionCliente(
        calle = data['calle'],
        barrio = data['barrio'],
        municipio = data['municipio'],
        departamento = data['departamento'],
        pais = data['pais'],
        informacion_adiccional = data['informacion_adiccional'],
        destinario = data['destinario'],
        fecha_creacion = data['fecha_creacion'],
        fecha_modificacion = data['fecha_modificacion'])
    db.session.add(new_direccioncliente)
    db.session.commit()
    return jsonify({'message': 'direccion de cliente created successfully'}), 201


@bp.route('/update/<int:id>', methods=['PUT'])
def update_metodopago(id):
    direccioncliente = DireccionCliente.query.get(id)
    if direccioncliente:
        data = request.json
        direccioncliente.calle = data['calle'],
        direccioncliente.barrio = data['barrio'],
        direccioncliente.municipio = data['municipio'],
        direccioncliente.departamento = data['departamento'],
        direccioncliente.pais = data['pais']
        direccioncliente.informacion_adiccional = data['informacion_adiccional']
        direccioncliente.destinario = data['destinario']
        direccioncliente.fecha_creacion = data['fecha_creacion']
        direccioncliente.fecha_modificacion = data['fecha_modificacion']
        db.session.commit()
        return jsonify({'message': 'direccion de cliente updated successfully'})
    return jsonify({'message': ' direccion de cliente not found'}), 404

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_producto(id):
    direccioncliente = DireccionCliente.query.get(id)
    if direccioncliente:
        db.session.delete(direccioncliente)
        db.session.commit()
        return jsonify({'message': 'direccion de cliente deleted successfully'})
    return jsonify({'message': 'direccion de cliente not found'}), 404


