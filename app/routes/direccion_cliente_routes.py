from flask import Blueprint, render_template, request, redirect,session, url_for, jsonify, flash
from flask_login import login_user, logout_user, current_user
from app.models.direccion_cliente import DireccionCliente
from app import db

bp = Blueprint('direccion_cliente', __name__)

@bp.route('/direccion_cliente/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        calle = request.form['calle']
        barrio = request.form['barrio']
        municipio = request.form['municipio']
        departamento = request.form['departamento']
        informacion_adicional = request.form['informacion_adicional']
        destinatario = request.form['destinatario']
        usuario_id = current_user.id
        
        new_direccion_cliente = DireccionCliente(calle=calle, barrio=barrio, municipio=municipio, departamento=departamento, informacion_adicional=informacion_adicional, destinatario=destinatario, usuario_id=usuario_id)
        db.session.add(new_direccion_cliente)
        db.session.commit()
        
        return redirect(url_for('pago.identificacion'))
    
    

@bp.route('/direccion_cliente/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    dataDC = DireccionCliente.query.get_or_404(id)

    if request.method == 'POST':
        dataDC.calle = request.form['calle']
        dataDC.barrio = request.form['barrio']
        dataDC.municipio = request.form['municipio']
        dataDC.departamento = request.form['departamento']
        dataDC.informacion_adicional = request.form['informacion_adicional']
        dataDC.destinatario = request.form['destinatario']


        db.session.commit()
        flash('Direccion actualizada con éxito', 'success')
        return redirect(url_for('pago.identificacion'))