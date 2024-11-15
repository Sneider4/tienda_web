from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.categoria import Categoria
from app.models.producto import Producto
from app import db
from flask_login import login_required, current_user
from app.models.producto import Producto

bp = Blueprint('categoria', __name__)

@bp.route('/categorias')
@login_required
def index():
    rol = current_user.rol 
    if(rol == "Administrador"):
        dataC = Categoria.query.all()
        totalC = Categoria.query.count()
        usuario = current_user
        return "categorias"
        #return render_template('categoria/index.html', dataC=dataC, totalC=totalC, usuario=usuario)
    else:
        return "error-------------------"
        #return redirect(url_for('producto.index'))
    

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
            
            return redirect(url_for('categoria.index'))

        return render_template('categoria/add.html')
    else:
        return redirect(url_for('producto.index'))

@bp.route('/categoria/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try: 
        if current_user.rol == "Administrador":
            categoria = Categoria.query.get_or_404(id)
            productos_asociados = Producto.query.filter_by(id=id).all()

            for producto in productos_asociados:
                db.session.delete(producto)
            
            db.session.delete(categoria)
            db.session.commit()
            flash('La categoría se eliminó exitosamente', 'info')

            return redirect(url_for('categoria.index'))
        else:
            return redirect(url_for('producto.index'))
    except:
        flash('La categoría no se puede eliminar porque se está usando el registro en otras tablas', 'danger')
        return redirect(url_for('categoria.index'))


@bp.route('/categoria/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.rol == "Administrador":
        categoria = Categoria.query.get_or_404(id)
        if request.method == 'POST':
            categoria.nombre = request.form['nombre']
            categoria.descripcion = request.form['descripcion']
            db.session.commit()
            # Redirige a la página anterior
            return redirect(url_for('categoria.index'))
        return render_template('categoria/edit.html', categoria=categoria)
    else:
        return redirect(url_for('producto.index'))
