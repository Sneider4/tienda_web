from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.categoria import Categoria
from app import db

bp = Blueprint('categoria', __name__)

@bp.route('/categoria')
def index():
    data = Categoria.query.all()
    return render_template('categoria/index.html', data=data)

@bp.route('/categoria/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        new_categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(new_categoria)
        db.session.commit()
        
        return redirect(url_for('producto.add'))

    return render_template('categoria/add.html')