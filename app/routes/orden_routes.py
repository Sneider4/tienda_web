from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
from app.models.orden import Orden
from app.models.carrito import Carrito
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
    
    dataCar = Carrito.query.filter_by(usuario_id=current_user.id).all()

    # Debugging: Print the form data to the console
    print(f"Usuario ID: {usuario_id}")
    print(f"Dirección ID: {direccion_id}")
    print(f"Método de Pago: {metodo_pago}")
    print(f"Carrito Items: {dataCar}")

    if not usuario_id or not direccion_id:
        return "Usuario ID o Dirección ID no proporcionados", 400

    if not dataCar:
        return "El carrito está vacío", 400

    total = 0.0
    productos = []

    for carrito in dataCar:
        print(f"Producto: {carrito}")
        producto_id, cantidad = carrito.split('-')
        cantidad = int(cantidad)
        
        producto = Producto.query.get(producto_id)
        
        if producto:
            total += producto.precio * cantidad
            productos.append({'producto_id': producto_id, 'cantidad': cantidad, 'precio': producto.precio})

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
<<<<<<< Updated upstream
=======

    print(f"Usuario ID: {usuario_id}")
    print(f"Dirección ID: {direccion_id}")
    print(f"Método de Pago: {metodo_pago}")
    print(f"Productos: {productos}")
    print(f"Total con Impuesto: {total_con_impuesto}")
    print(f"Carrito Items: {carrito_items}")
>>>>>>> Stashed changes
    
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
   orden=Orden.query.order_by(Orden.id.desc()).first()
   return render_template('pago/factura.html', orden=orden)