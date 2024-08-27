from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app.models.usuario import Usuario
from app import db

bp = Blueprint('usuario', __name__)

@bp.route('/usuario')
def index():
    data = Usuario.query.all()
    return render_template('usuario/index.html', data=data)

@bp.route('/usuario/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo_electronico']
        telefono = request.form['telefono']
        contrasena = request.form['contrasena']
        departamento = request.form['departamento']
        ciudad = request.form['ciudad']
        genero = request.form['genero']
        fecha_nacimiento = request.form['fecha_nacimiento']
        
        new_usuario = Usuario(nombre=nombre, apellido=apellido, correo_electronico=correo_electronico, telefono=telefono, contrasena=contrasena, departamento=departamento, ciudad=ciudad, genero=genero, fecha_nacimiento=fecha_nacimiento)
        db.session.add(new_usuario)
        db.session.commit()
        
        return redirect(url_for('producto.index'))

    return render_template('usuario/registrar.html')

@bp.route('/usuario/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']
        
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico).first()

        if usuario and check_password_hash(usuario.contrasena, contrasena):
            login_user(usuario)
            flash("Login successful!", "success")
            return redirect(url_for('usuario.dashboard'))
        
        flash('Invalid credentials. Please try again.', 'danger')
    
    if current_user.is_authenticated:
        return redirect(url_for('usuario.dashboard'))
    
    return render_template("producto/index.html")

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', email=current_user.correo_electronico)

# Ruta de Logout
@bp.route('/logout')
def logout():
    logout_user() 
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('usuario.login'))