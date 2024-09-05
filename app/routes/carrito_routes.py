from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from flask_login import login_user, logout_user, current_user
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
        producto_id = request.form['idP']
        cantidad = request.form['cantidad']
        usuario_id = current_user.id

        new_carrito = Carrito(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
        db.session.add(new_carrito)
        db.session.commit()

        carrito_items = Carrito.query.filter_by(usuario_id=usuario_id).all()

        total_items = sum(item.cantidad for item in carrito_items)
        session['total_items'] = total_items

        producto = Producto.query.filter_by(id=producto_id).first()
        flash(f'{producto.nombre} agregado exitosamente.', 'success')
        
        return redirect(url_for('producto.index'))
    
@bp.route('/carrito/delete/<int:id>')
def delete(id):
    carrito = Carrito.query.get_or_404(id)
    
    db.session.delete(carrito)
    db.session.commit()

    return redirect(url_for('producto.index'))