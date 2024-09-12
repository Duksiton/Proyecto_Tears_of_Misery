from flask import Blueprint, request, jsonify, session
from mvc.model.db_connection import create_connection, close_connection

compras_controller = Blueprint('compras_controller', __name__)

@compras_controller.route('/api/guardar_compra', methods=['POST'])
def guardar_compra():
    if 'idUsuario' not in session:
        return jsonify({'success': False, 'message': 'Usuario no logueado'}), 401

    data = request.json
    id_usuario = session['idUsuario']
    productos = data.get('productos', [])
    total = data.get('total', 0)
    fecha_compra = data.get('fechaCompra', '')

    print("Datos recibidos:", data)  # Imprime los datos recibidos

    if not productos:
        return jsonify({'success': False, 'message': 'No hay productos en la compra'}), 400

    conn = create_connection()
    cursor = conn.cursor()

    try:
        for producto in productos:
            print("Producto:", producto)  # Imprime cada producto

            id_producto = producto.get('idProducto')
            nombre_producto = producto.get('nombreProducto', '')
            imagen_producto = producto.get('imagenProducto', '')
            cantidad = producto.get('cantidad', 0)
            total_producto = producto.get('total', 0)

            cursor.execute('''
                INSERT INTO historial_compras (idUsuario, idProducto, nombreProducto, imagenProducto, fechaCompra, cantidad, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (id_usuario, id_producto, nombre_producto, imagen_producto, fecha_compra, cantidad, total_producto))

        conn.commit()
        return jsonify({'success': True, 'message': 'Compra guardada exitosamente'}), 200

    except Exception as e:
        conn.rollback()
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        close_connection(conn)
