from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.producto import Producto
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('productosocket', __name__, url_prefix='/Productosockets')

@bp.route('/index', methods=['GET'])
def get_producto():
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_producto():
    data = request.json
    new_producto = Producto(
        nombre = data['nombre'],
        descripcion = data['descripcion'],
        precio = data['precio'],
        stock = data['stock'],
        categoria = data['categoria'],
        imagen = data['imagen'])
    db.session.add(new_producto)
    db.session.commit()
    return jsonify({'message': 'Producto created successfully'}), 201

@bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    producto = Producto.query.get(id)
    if producto:
        data = request.json
        producto.nombre = data['nombre']
        producto.descripcion = data['descripcion']
        producto.precio = data['precio']
        producto.stock = data['stock']
        producto.categoria = data['categoria']
        producto.imagen = data['imagen']
        db.session.commit()
        return jsonify({'message': 'Producto updated successfully'})
    return jsonify({'message': ' Producto not found'}), 404

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'message': 'Producto deleted successfully'})
    return jsonify({'message': 'Producto not found'}), 404

