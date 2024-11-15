from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.categoria import Categoria
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('categoriasocket', __name__, url_prefix='/Categoriasockets')

@bp.route('/index', methods=['GET'])
def get_category():
    categorias = Categoria.query.all()
    return jsonify([categoria.to_dict() for categoria in categorias ]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_category():
    data = request.json
    new_categoria = Categoria(
        nombre=data['nombre'], 
        descripcion=data['descripcion'])
    db.session.add(new_categoria)
    db.session.commit()
    return jsonify({'message': 'Category created successfully'}), 201

@bp.route('/update/<int:id>', methods=['PUT'])
def update_category(id):
    categoria = Categoria.query.get(id)
    if categoria:
        data = request.json
        categoria.nombre = data['nombre']
        categoria.descripcion = data['descripcion']
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'})
    return jsonify({'message': 'Category not found'}), 404

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_category(id):
    categoria = Categoria.query.get(id)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'message': 'category deleted successfully'})
    return jsonify({'message': 'category not found'}), 404