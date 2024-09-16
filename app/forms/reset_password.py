from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RequestResetForm(FlaskForm):
    correo_electronico = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar restablecimiento de contraseña')

class ResetPasswordForm(FlaskForm):
    contrasena = PasswordField('Nueva Contraseña', validators=[DataRequired()])
    confirmar_contrasena = PasswordField('Confirma tu Contraseña', validators=[DataRequired(), EqualTo('contrasena', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Restablecer contraseña')