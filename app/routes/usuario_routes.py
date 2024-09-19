from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session, current_app
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from app.forms.reset_password import RequestResetForm, ResetPasswordForm
from werkzeug.security import check_password_hash
from app.models.usuario import Usuario
from app import mail
from app import db
import app

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
    
    secret_key = current_app.config['SECRET_KEY']
    print(f"SECRET_KEY: {secret_key}")
    print("1--------------")
    if request.method == 'POST':
        print("2")
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']
        print("3")
        print(f"4 correo {correo_electronico} contraseña: {contrasena}")
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico, contrasena=contrasena).first()
        if usuario:
            print("5")
            login_user(usuario)
            flash(f"Bienvenido, {usuario.nombre} {usuario.apellido}!" , "success")
            if usuario.rol == "Cliente":
                print("Entra a cliente")
                return redirect(url_for('producto.index'))
            elif usuario.rol == "Administrador":
                return redirect(url_for('admin.index'))
            else:
                flash('Credenciales invalidos. Intente nuevamente.', 'danger')
        else:
            flash('No se a encontrado un usuario', 'danger')

    if current_user.is_authenticated:
        return redirect(url_for('usuario.dashboard'))
    
    return render_template("producto/index.html")

@bp.route('/dashboard')
def dashboard():
    return render_template('producto/index.html', email=current_user.correo_electronico)

# Ruta de Logout
@bp.route('/logout')
def logout():
    logout_user() 
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('producto.index'))

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    print("1", form.validate_on_submit())

    if form.validate_on_submit():

        usuario = Usuario.query.filter_by(correo_electronico=form.correo_electronico.data).first()
        if usuario:
            token = usuario.get_reset_token()
            msg = Message('Solicitud de restablecimiento de contraseña',
                          sender='programanike@gmail.com',
                          recipients=[usuario.correo_electronico])
            msg.body = f'''Para restablecer tu contraseña, haz clic en el siguiente enlace:
                        
                        {url_for('usuario.reset_token', token=token, _external=True)}

                        Si no solicitaste este cambio, simplemente ignora este correo.
                        '''
            try:
                print("Enviando correo...")

                mail.send(msg)
                print("Correo enviado exitosamente")
                flash('El enlace para restablecer la contraseña ha sido enviado a tu correo electrónico.', 'info')
                return redirect(url_for('producto.index'))
            except Exception as e:
                print(f"Error al enviar el correo: {str(e)}")
                flash('Hubo un error al intentar enviar el correo. Por favor, intenta nuevamente.', 'danger')

            return render_template('producto/index.html', form = form)
    return render_template('usuario/reset_request.html', form = form)

@bp.route('/reset/<token>', methods=['POST', 'GET'])
def reset_token(token):
    print("entra al reset token")
    print('1', current_user.is_authenticated )
    print(f"token {token}")
    formulario = ResetPasswordForm()
    
    if current_user.is_authenticated:
        print('-----------------------------------------------------------')
        return redirect(url_for('main.index')), print("Ayuda")
    if request.method == 'POST':
        
        usuario = Usuario.verify_reset_token(token)
        print('3 entra al post')
        if usuario is None:
            print('4')
            flash('El enlace es inválido o ha expirado.', 'warning')
            print('5')
            return redirect(url_for('usuario.reset_request')), print("JAJA")
        
        print(formulario)
        print(f'6 ------- {formulario.validate_on_submit()}----metodo ------- {request.method}')
        print(f"Contraseña --------------------{formulario.contrasena.data}-------")
        if formulario.validate_on_submit():
            usuario.contrasena = formulario.contrasena.data
            db.session.commit()
            flash('Tu contraseña ha sido actualizada. ¡Ahora puedes iniciar sesión!', 'success')
            print('7')
            return redirect(url_for('producto.index')), print("Prueba")
        else:
            print("Errores del formulario:", formulario.errors)
            print(formulario)
        
            # Depurar errores del formulario si la validación falla
        if formulario.errors:
            print(formulario.errors)
        print('8')
    return render_template('usuario/reset_token.html', form=formulario, token=token, _external=True)