import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from mvc.model.db_connection import create_connection
from mysql.connector import Error

historial_compras_controller = Blueprint('historial_compras_controller', __name__)

@historial_compras_controller.route('/historial_compras', methods=['GET'])
def historial_compras():
    idUsuario = session.get('idUsuario')
    
    if not idUsuario:
        return redirect(url_for('login_controller.login'))  # Redirige a iniciar sesión si no hay un usuario autenticado

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT idCompra, nombreProducto, imagenProducto, fechaCompra, cantidad, total, estado
        FROM historial_compras
        WHERE idUsuario = %s
        """
        cursor.execute(query, (idUsuario,))
        compras = cursor.fetchall()
    except Exception as e:
        print('Error al obtener historial de compras:', e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('perfil.perfil') + '#compras')

@historial_compras_controller.route('/registrar_compra', methods=['POST'])
def registrar_compra():
    idUsuario = session.get('idUsuario')
    if not idUsuario:
        return redirect(url_for('login_controller.login'))  # Redirige si no hay usuario autenticado

    idProducto = request.form.get('idProducto')
    nombreProducto = request.form.get('nombreProducto')
    imagenProducto = request.form.get('imagenProducto')
    cantidad = int(request.form.get('cantidad'))
    total = float(request.form.get('total'))
    fechaCompra = datetime.date.today()
    estado = 'Pendiente'  # Estado por defecto

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Inserción en la tabla historial_compras
        query = """
        INSERT INTO historial_compras (idUsuario, idProducto, nombreProducto, imagenProducto, fechaCompra, cantidad, total, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (idUsuario, idProducto, nombreProducto, imagenProducto, fechaCompra, cantidad, total, estado))
        conn.commit()
       
    except Error as e:
        flash(f'Error al registrar la compra: {e}')
    finally:
        cursor.close()
        conn.close()

    # Redirige al perfil del usuario a la sección de historial de compras
    return redirect(url_for('perfil.perfil') + '#compras') # Redirige a la página de historial de compras
