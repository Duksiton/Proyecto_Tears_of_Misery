from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from mvc.model.db_connection import create_connection
from mysql.connector import Error

# Crear el blueprint para el controlador de perfil
perfil_controller = Blueprint('perfil', __name__, template_folder='templates/usuario')

@perfil_controller.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    connection = create_connection()

    if request.method == 'POST':
        return actualizar_perfil(user)

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedido WHERE idUsuario = %s", (user['idUsuario'],))
    pedidos = cursor.fetchall()

    return render_template('usuario/perfil.html', user=user, pedidos=pedidos)

def actualizar_perfil(user):
    # Obtén los datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    user_id = user['idUsuario']

    connection = create_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('''UPDATE usuario
                          SET nombre = %s, email = %s, direccion = %s, telefono = %s
                          WHERE idUsuario = %s''',
                       (nombre, email, direccion, telefono, user_id))
        connection.commit()

        # Actualiza la sesión con los nuevos datos
        user['nombre'] = nombre
        user['email'] = email
        user['direccion'] = direccion
        user['telefono'] = telefono
        session['user'] = user

        flash("Perfil actualizado exitosamente.")
    except Error as e:
        flash(f"Error al actualizar el perfil: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Redirige de nuevo a la página de perfil
    return redirect(url_for('perfil.perfil'))

# Asegúrate de registrar este controlador en tu aplicación Flask
# app.register_blueprint(perfil_controller)


@perfil_controller.route('/api/realizar_pedido', methods=['POST'])
def realizar_pedido():
    data = request.json
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Inserta el pedido
        cursor.execute("""
            INSERT INTO pedido (fechaPedido, totalPedido, estado, idUsuario)
            VALUES (CURDATE(), %s, 'pendiente', %s)
        """, (data['precio_total'], data['user_id']))
        id_pedido = cursor.lastrowid  # Obtener el ID del último pedido insertado

        # Inserta los productos del pedido
        for producto in data['productos']:
            cursor.execute("""
                INSERT INTO pedido_producto (idPedido, idProducto, cantidad)
                VALUES (%s, %s, %s)
            """, (id_pedido, producto['idProducto'], producto['cantidad']))

        conn.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        print("Error al insertar en la base de datos:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
