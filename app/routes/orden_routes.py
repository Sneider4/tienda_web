from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.orden import Orden
from app import db
from app.models.producto import Producto
from app.models.detalle_orden import DetalleOrden

bp = Blueprint('orden', __name__)

@bp.route('/orden')
def index():
    data = Orden.query.all()
    return render_template('orden/index.html', data=data)

@bp.route('/generar_orden', methods=['GET'])
def generar_orden():
    print('1')
    usuario_id = request.form.get('usuario_id')  # ID del usuario
    direccion_id = request.form.get('direccion_id')  # ID de la dirección seleccionada
    carrito = request.form.getlist('carrito')  # Lista de productos en el carrito

    total = 0
    orden = Orden(usuario_id=usuario_id, direccion_id=direccion_id, total=total)
    db.session.add(orden)
    db.session.flush()  # Para obtener el ID de la factura antes de hacer commit

    # Procesar los productos del carrito
    for item in carrito:
        producto_id, cantidad = item.split('-')
        producto = Producto.query.get(producto_id)
        cantidad = int(cantidad)
        precio_unitario = producto.precio
        total += cantidad * precio_unitario

        detalle = DetalleOrden(factura_id=orden.id, producto_id=producto.id, cantidad=cantidad, precio_unitario=precio_unitario)
        db.session.add(detalle)

    # Actualizar el total de la factura
    orden.total = total
    db.session.commit()

    return redirect(url_for('mostrar_factura', orden_id=orden.id))

@bp.route('/mostrar_factura/<int:orden_id>')
def mostrar_factura(orden_id):
    orden = Orden.query.get_or_404(orden_id)
    detalles = DetalleOrden.query.filter_by(orden_id=orden_id).all()
    return render_template('pago/factura.html', orden=orden, detalles=detalles)