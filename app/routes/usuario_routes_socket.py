from flask import Blueprint, redirect, request, render_template, url_for, jsonify, send_file
from app.models.usuario import Usuario
from app import db
from io import BytesIO
import base64
import json

bp = Blueprint('usuariosocket', __name__, url_prefix='/Usuariosockets')

@bp.route('/index', methods=['GET'])
def get_user():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200, {'content-Type': 'application/json'}

@bp.route('/add', methods=['POST'])
def create_user():
    data = request.json
    new_usuario = Usuario(
        nombre=data['nombre'], 
        apellido=data['apellido'],
        telefono=data['telefono'], 
        correo_electronico=data['correo_electronico'],
        contrasena=data['contrasena'], 
        departamento=data['departamento'], 
        ciudad=data['ciudad'], 
        genero=data['genero'], 
        fecha_nacimiento=data['fecha_nacimiento'], 
        rol=data['rol'], 
        imagen=data['imagen'])
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    usuario = Usuario.query.get(id)
    if usuario:
        data = request.json
        usuario.nombre = data['nombre']
        usuario.apellido = data['apellido']
        usuario.correo_electronico = data['correo_electronico']
        usuario.telefono = data['telefono']
        usuario.contrasena = data['contrasena']
        usuario.departamento = data['departamento']
        usuario.ciudad = data['ciudad']
        usuario.genero = data['genero']
        usuario.fecha_nacimiento = data['fecha_nacimiento']
        usuario.rol = data['rol']
        usuario.imagen = data['imagen']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Usuario.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404