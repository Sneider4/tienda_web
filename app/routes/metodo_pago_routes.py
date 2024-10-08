from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, current_user
from app.models.metodo_pago import MetodoPago
from app import db

bp = Blueprint('metodo_pago', __name__)

@bp.route('/metodo_pago/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        tipo = request.form['tipo']
        numero_tarjeta = request.form['numero_tarjeta']
        nombre_tarjeta = request.form['nombre_tarjeta']
        fecha_vencimiento = request.form['fecha_vencimiento']
        codigo_seguridad = request.form['codigo_seguridad']
        usuario_id = current_user.id
        
        new_metodo_pago = MetodoPago(tipo=tipo, numero_tarjeta=numero_tarjeta, nombre_tarjeta=nombre_tarjeta, fecha_vencimiento=fecha_vencimiento, codigo_seguridad=codigo_seguridad, usuario_id=usuario_id)
        db.session.add(new_metodo_pago)
        db.session.commit()
        
        return redirect(url_for('pago.identificacion'))
    


@bp.route('/metodo_pago/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    dataMT = MetodoPago.query.get_or_404(id)

    if request.method == 'POST':
        dataMT.tipo = request.form['tipo']
        dataMT.numero_tarjeta = request.form['numero_tarjeta']
        dataMT.nombre_tarjeta = request.form['nombre_tarjeta']
        dataMT.fecha_vencimiento = request.form['fecha_vencimiento']
        dataMT.codigo_seguridad = request.form['codigo_seguridad']


        db.session.commit()
        flash('Metodo de pago actualizado con éxito', 'success')
        return redirect(url_for('pago.identificacion'))