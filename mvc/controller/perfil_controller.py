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
        if request.form.get('action') == 'update_profile':
            return actualizar_perfil()
        elif request.form.get('action') == 'crear_pedido':
            return crear_pedido()

    # Obtener los pedidos del usuario
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedido WHERE idUsuario = %s", (user['idUsuario'],))
    pedidos = cursor.fetchall()

    return render_template('usuario/perfil.html', user=user, pedidos=pedidos)

def actualizar_perfil():
    # Verifica si el usuario está autenticado
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    # Obtén los datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    user_id = user['idUsuario']

    try:
        # Conecta a la base de datos
        conn = create_connection()
        cursor = conn.cursor()

        # Actualiza los datos del usuario
        cursor.execute('''UPDATE usuario
                          SET nombre = %s, email = %s, direccion = %s, telefono = %s
                          WHERE idUsuario = %s''',
                       (nombre, email, direccion, telefono, user_id))
        conn.commit()

        # Actualiza la sesión con los nuevos datos
        user['nombre'] = nombre
        user['email'] = email
        user['direccion'] = direccion
        user['telefono'] = telefono
        session['user'] = user

        flash("Perfil actualizado exitosamente.")
    except Exception as e:
        # Manejo de errores: imprime el error en el registro
        print(f'Error al actualizar perfil: {e}')
        conn.rollback()
        flash("Error al actualizar perfil. Inténtalo de nuevo.")
    finally:
        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()

    # Redirige de nuevo a la página de perfil
    return redirect(url_for('perfil.perfil'))

def crear_pedido():
    # Verifica si el usuario está autenticado
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    # Obtén los datos del pedido desde el formulario
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad'))
    precio_total = float(request.form.get('precio_total'))

    try:
        # Conecta a la base de datos
        conn = create_connection()
        cursor = conn.cursor()

        # Insertar el pedido en la tabla pedido
        fecha_pedido = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            'INSERT INTO pedido (fechaPedido, totalPedido, estado, idUsuario) VALUES (%s, %s, %s, %s)',
            (fecha_pedido, precio_total, 'Completado', user['idUsuario'])
        )
        id_pedido = cursor.lastrowid  # Obtener el ID del último pedido insertado

        # Insertar el detalle del pedido
        cursor.execute(
            'INSERT INTO detallePedido (cantidad, precio, idProducto, idPedido) VALUES (%s, %s, %s, %s)',
            (cantidad, precio_total / cantidad, producto_id, id_pedido)
        )

        # Confirmar los cambios en la base de datos
        conn.commit()
        flash("Pedido realizado exitosamente.")
    except Exception as e:
        # Manejo de errores: imprime el error en el registro
        print(f'Error al crear pedido: {e}')
        conn.rollback()
        flash("Error al crear pedido. Inténtalo de nuevo.")
    finally:
        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()

    # Redirige de nuevo a la página de perfil
    return redirect(url_for('perfil.perfil'))

# Asegúrate de registrar este controlador en tu aplicación Flask
# app.register_blueprint(perfil_controller)
