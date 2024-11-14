from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.carrito import Carrito
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('carritosocket', __name__, url_prefix='/Carritosockets')

@bp.route('/index', methods=['GET'])
def get_carrito():
    carritos = Carrito.query.all()
    return jsonify([carrito.to_dict() for carrito in carritos]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_carrito():
    data = request.json
    new_carrito = Carrito(
        usuario_id=data['usuario_id'], 
        producto_id=data['producto_id'],
        cantidad=data['cantidad'])
    db.session.add(new_carrito)
    db.session.commit()
    return jsonify({'message': 'Carrito created successfully'}), 201

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_carrito(id):
    carrito = Carrito.query.get(id)
    if carrito:
        db.session.delete(carrito)
        db.session.commit()
        return jsonify({'message': 'Carrito deleted successfully'})
    return jsonify({'message': 'Carrito not found'}), 404
