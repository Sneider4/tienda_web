from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.carrito import Carrito
from app.models.producto import Producto
from app.models.usuario import Usuario
from app import db

bp = Blueprint('carrito', __name__)

@bp.route('/carrito')
def index():
    data = Carrito.query.all()
    dataP = Producto.query.all()
    dataU = Usuario.query.all()
    return render_template('carrito/index.html', data=data, dataP=dataP, dataU=dataU)

@bp.route('/carrito/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        print("entra a post")
        print(request)
        usuario_id = request.form['idU']
        producto_id = request.form['idP']
        cantidad = request.form['cantidad']
        print(f"{usuario_id}")
        new_carrito = Carrito(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
        db.session.add(new_carrito)
        db.session.commit()
        
        return redirect(url_for('producto.index'))