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


@bp.route('/orden/generar_orden', methods=['POST'])
def generar_orden():
    usuario_id = request.form.get('usuario_id')
    direccion_id = request.form.get('direccion_id')
    metodo_pago = request.form.get('metodo_pago')
    
    carrito_items = request.form.getlist('carrito')

    total = 0.0
    productos = []

    for item in carrito_items:
        print(f"Producto: {item}")
        producto_id, cantidad = item.split('-')
        cantidad = int(cantidad)
        
        producto = Producto.query.get(producto_id)
        
        if producto:
            total += producto.precio * cantidad
            productos.append({'producto_id': producto_id, 'cantidad': cantidad})

    impuesto = total * 0.19
    total_con_impuesto = total + impuesto

    nueva_orden = Orden(
        usuario_id=usuario_id,
        direccion_id=direccion_id,
        metodo_pago=metodo_pago,
        total=total_con_impuesto 
    )

    db.session.add(nueva_orden)
    db.session.commit()

    guardar_detalle_orden(nueva_orden.id, productos)
    
    return redirect(url_for('orden.orden_confirmada'))


def guardar_detalle_orden(orden_id, productos):
    
    for producto in productos:
        print(f"Guardando detalle de orden: {producto}")
        detalle_orden = DetalleOrden(
            orden_id=orden_id,
            producto_id=producto['producto_id'],
            cantidad=producto['cantidad'],
            precio=producto['precio']
        )
        db.session.add(detalle_orden)
    
    db.session.commit()


@bp.route('/orden/confirmada')
def orden_confirmada():
   return render_template('pago/factura.html')