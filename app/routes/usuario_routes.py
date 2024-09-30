from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session, current_app
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from app.forms.reset_password import RequestResetForm, ResetPasswordForm
from werkzeug.security import check_password_hash
from app.models.usuario import Usuario
from app import mail
from app import db
import app
import os, app

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
        imagen = request.files['imagen']  # Para obtener la imagen del formulario
        
        # Asignar imagen por defecto dependiendo del género si no se sube una imagen
        if imagen.filename == '':
            if genero == 'masculino':
                imagen_path = '../static/images/avatar-hombre.jpeg'  # Imagen por defecto masculina
            elif genero == 'femenino':
                imagen_path = '../static/images/avatar-mujer.jpeg'  # Imagen por defecto femenina
            else:
                imagen_path = '../static/images/avatar-gay.jpeg'  # Imagen por defecto para otro género
        else:
            # Si se subió una imagen, guardar la imagen en una carpeta
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static', 'images', filename)
            imagen.save(os.path.join(os.path.dirname(__file__), '..', imagen_path))
            ruta_imagen = imagen_path  # Guardar la imagen en la carpeta 'static/uploads'
        
        new_usuario = Usuario(
            nombre=nombre, 
            apellido=apellido, 
            correo_electronico=correo_electronico, 
            telefono=telefono,
            contrasena=contrasena, 
            departamento=departamento, 
            ciudad=ciudad, 
            genero=genero, 
            fecha_nacimiento=fecha_nacimiento,
            imagen=imagen_path)
        db.session.add(new_usuario)
        db.session.commit()
        
        return redirect(url_for('producto.index'))

    return render_template('usuario/registrar.html')

@bp.route('/usuario/delete/<int:id>', methods=['POST'])
def delete(id):    
    usuario = Usuario.query.get_or_404(id)
            
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado con éxito', 'success')
    return redirect(url_for('admin.clientes'))

@bp.route('/usuario/login', methods=['GET', 'POST'])
def login():
    
    secret_key = current_app.config['SECRET_KEY']
    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico, contrasena=contrasena).first()
        if usuario:
            login_user(usuario)
            
            if usuario.rol == "Cliente":
                return redirect(url_for('producto.index'))

            elif usuario.rol == "Administrador":
                flash(f"Bienvenido Administrador, {usuario.nombre} {usuario.apellido}!" , "success")
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
    flash('Has cerrado sesión.', 'danger')
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Ruta para cambiar el avatar del usuario
@bp.route('/usuario/cambiar_imagen/<int:id>', methods=['GET', 'POST'])
def cambiar_imagen(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        # Verifica si se subió un archivo
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Verifica si se seleccionó un archivo
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Guardar el archivo en una ubicación segura
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'images')
            
            # Crear el directorio si no existe
            os.makedirs(upload_folder, exist_ok=True)
            
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            # Actualizar el campo "imagen" en el usuario
            usuario.imagen = filename
            db.session.commit()
            
            flash('Imagen de perfil actualizada correctamente')
            return redirect(url_for('usuario.cambiar_imagen', id=id))
    
    return render_template('administrador/configuraciones.html', usuario=usuario)