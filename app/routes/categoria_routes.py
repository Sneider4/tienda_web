from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.categoria import Categoria
from app import db
from flask_login import login_required, current_user

bp = Blueprint('categoria', __name__)

@bp.route('/categoria')
@login_required
def index():
    rol = current_user.rol 
    if(rol == "Administrador"):
        data = Categoria.query.all()
        return render_template('categoria/index.html', data=data)
    else:
        return redirect(url_for('producto.index'))

@bp.route('/categoria/add', methods=['GET', 'POST'])
@login_required
def add():
    rol = current_user.rol 
    if(rol == "Administrador"):

        if request.method == 'POST':
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            
            new_categoria = Categoria(nombre=nombre, descripcion=descripcion)
            db.session.add(new_categoria)
            db.session.commit()
            
            return redirect(url_for('admin.layout_static'))

        return render_template('categoria/add.html')
    else:
        return redirect(url_for('producto.index'))
    
