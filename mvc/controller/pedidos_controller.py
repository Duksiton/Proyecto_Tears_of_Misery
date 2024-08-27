# Controlador de pedidos
from flask import Blueprint, render_template, request, redirect, url_for, flash
from mvc.model.db_connection import create_connection

pedidos_controller = Blueprint('pedidos', __name__, template_folder='templates/admin')

@pedidos_controller.route('/pedidos', methods=['GET'])
def index():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedido")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin/pedidos.html', pedidos=pedidos)

@pedidos_controller.route('/pedidos/<int:id>', methods=['GET'])
def edit(id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedido WHERE idPedido = %s", (id,))
    pedido = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('admin/pedidos.html', pedido=pedido)

@pedidos_controller.route('/pedidos', methods=['POST'])
def create_or_update():
    pedido_id = request.form.get('pedidoId')
    fecha_pedido = request.form.get('fechaPedido')
    total_pedido = request.form.get('totalPedido')
    estado = request.form.get('estado')
    id_usuario = request.form.get('idUsuario')

    conn = create_connection()
    cursor = conn.cursor()

    if pedido_id:
        # Actualizar
        cursor.execute("""
            UPDATE pedido
            SET fechaPedido = %s, totalPedido = %s, estado = %s, idUsuario = %s
            WHERE idPedido = %s
        """, (fecha_pedido, total_pedido, estado, id_usuario, pedido_id))
    else:
        # Crear
        cursor.execute("""
            INSERT INTO pedido (fechaPedido, totalPedido, estado, idUsuario)
            VALUES (%s, %s, %s, %s)
        """, (fecha_pedido, total_pedido, estado, id_usuario))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pedidos.index'))

@pedidos_controller.route('/pedidos/<int:id>', methods=['POST'])
def delete(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedido WHERE idPedido = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pedidos.index'))



