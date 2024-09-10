# Importaciones
from flask import Flask, abort, render_template, flash, jsonify, request,session,redirect, url_for
from mvc.model.db_connection import create_connection, close_connection
from mvc.controller.producto_controller import producto_controller
from mvc.controller.usuarios_controller import usuarios_controller, verificar_usuario
from mvc.controller.login_controller import login_controller
from mvc.controller.registro_controller import registro_controller
from mvc.controller.perfil_controller import perfil_controller
from mvc.controller.logout_controller import logout_controller
from mvc.controller.perfil_controller import perfil_controller
from mvc.controller.pedidos_controller import pedidos_controller
from mvc.controller.compras_controller import compras_controller
import shutil
import os

import bcrypt

app = Flask(__name__)
app.secret_key = 'tearsofmiseryconexion'

# Registro de los blueprints
app.register_blueprint(producto_controller)
app.register_blueprint(usuarios_controller)
app.register_blueprint(login_controller)
app.register_blueprint(registro_controller)
app.register_blueprint(perfil_controller)
app.register_blueprint(logout_controller)
app.register_blueprint(pedidos_controller)
app.register_blueprint(compras_controller)






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/inicio')
def inicio():
    return render_template('usuario/inicio.html')

@app.route('/catalogo')
def catalogo():
    return render_template('usuario/catalogo.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/producto/<int:id>')
def mostrar_producto(id):
    return producto_controller.producto(id)

@app.route('/catalogo')
def mostrar_catalogo():
    return producto_controller.catalogo()

@app.route('/verificacion/<int:id>')
def verificacion(id):
    return verificar_usuario(id)  # Redirige a la función que proporciona los datos del usuario


@app.route('/api/guardar_compra', methods=['POST'])
def guardar_compra():
    try:
        data = request.get_json()
        productos = data.get('productos', [])
        total = data.get('total', 0)
        fechaCompra = data.get('fechaCompra', None)

        conn = create_connection()
        cursor = conn.cursor()

        for producto in productos:
            ruta_imagen_original = os.path.join('static', 'images', 'productos-insertados', producto['imagenProducto'])
            nombre_imagen_historial = producto['imagenProducto']
            ruta_imagen_historial = os.path.join('static', 'images', 'historial', nombre_imagen_historial)

            if not os.path.isfile(ruta_imagen_original):
                print(f"Imagen no encontrada: {ruta_imagen_original}")
                continue

            os.makedirs(os.path.dirname(ruta_imagen_historial), exist_ok=True)

            try:
                shutil.copy2(ruta_imagen_original, ruta_imagen_historial)  
                print(f"Imagen copiada a {ruta_imagen_historial}")
            except FileNotFoundError:
                print(f"Error: La imagen original no existe - {ruta_imagen_original}")
            except PermissionError:
                print(f"Error: Sin permisos para copiar la imagen - {ruta_imagen_original}")
            except Exception as e:
                print(f"Error inesperado al copiar la imagen: {e}")
                continue

            query = """
            INSERT INTO historial_compras (idUsuario, idProducto, nombreProducto, imagenProducto, fechaCompra, cantidad, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                producto['idUsuario'],
                producto['idProducto'],
                producto['nombreProducto'],
                nombre_imagen_historial,
                fechaCompra,
                producto['cantidad'],
                "{:,.0f}".format(float(producto['total']))
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Compra guardada con éxito'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT hc.idCompra, hc.nombreProducto, hc.fechaCompra, u.email, hc.total, hc.estado FROM historial_compras hc JOIN usuario u ON hc.idUsuario = u.idUsuario"
        cursor.execute(query)
        pedidos = cursor.fetchall()
        pedidos_formateados = []
        for pedido in pedidos:
            fecha_formateada = pedido[2].strftime('%Y-%m-%d')  # Formatear fecha
            total_formateado = "${:,.3f} ".format(pedido[4])  # Formatear precio
            pedidos_formateados.append({
                'idCompra': pedido[0],
                'nombreProducto': pedido[1],
                'fechaCompra': fecha_formateada,
                'email': pedido[3],
                'total': total_formateado,
                'estado': pedido[5]
            })
        cursor.close()
        conn.close()
        return jsonify(pedidos_formateados)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    

@app.route('/api/actualizar_pedido', methods=['POST'])
def actualizar_pedido():
    try:
        data = request.form
        idPedido = data.get('idPedido')
        estado = data.get('estado')
        conn = create_connection()
        cursor = conn.cursor()
        query = "UPDATE historial_compras SET estado = %s WHERE idCompra = %s"
        cursor.execute(query, (estado, idPedido))
        conn.commit()
        cursor.close()
        conn.close()
        return '', 204  # Devolvemos una respuesta vacía con código 204
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    
@app.route('/api/historial-compras', methods=['GET'])
def get_historial_compras():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 5))
        offset = (page - 1) * items_per_page
        search_query = request.args.get('query', '')

        # Construcción de la consulta con búsqueda y paginación
        query = """
        SELECT hc.idCompra, hc.nombreProducto, hc.fechaCompra, u.email, hc.total, hc.estado
        FROM historial_compras hc
        JOIN usuario u ON hc.idUsuario = u.idUsuario
        WHERE hc.idCompra LIKE %s OR hc.nombreProducto LIKE %s OR hc.fechaCompra LIKE %s OR u.email LIKE %s OR hc.total LIKE %s
        LIMIT %s OFFSET %s
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (like_query, like_query, like_query, like_query, like_query, items_per_page, offset))
        historial_compras = cursor.fetchall()

        # Consulta para obtener el total de historial de compras sin paginación
        count_query = """
        SELECT COUNT(*) AS total
        FROM historial_compras hc
        JOIN usuario u ON hc.idUsuario = u.idUsuario
        WHERE hc.idCompra LIKE %s OR hc.nombreProducto LIKE %s OR hc.fechaCompra LIKE %s OR u.email LIKE %s OR hc.total LIKE %s
        """
        cursor.execute(count_query, (like_query, like_query, like_query, like_query, like_query))
        total = cursor.fetchone()['total']

        return jsonify({'historial_compras': historial_compras, 'total': total})
    except Exception as e:
        print('Error al obtener historial de compras:', e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/actualizar_pedido', methods=['POST'])
def actualizar_estado_pedido():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        id_pedido = request.form['idPedido']
        estado = request.form['estado']

        query = """
        UPDATE historial_compras
        SET estado = %s
        WHERE idCompra = %s
        """
        cursor.execute(query, (estado, id_pedido))
        conn.commit()

        return jsonify({'mensaje': 'Estado actualizado correctamente'})
    except Exception as e:
        print('Error al actualizar estado:', e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/productos')
def mostrar_productos():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/check_product/<int:id_producto>', methods=['GET'])
def check_product(id_producto):
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        abort(500, description="Error de conexión a la base de datos")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE idProducto = %s", (id_producto,))
        producto = cursor.fetchone()  # Obtener un solo producto por ID

        if not producto:
            flash("Producto no encontrado")
            return redirect(url_for('productos'))  # Redirigir a la lista de productos si no se encuentra

    except Exception as e:
        flash(f"Error al obtener el producto: {str(e)}")
        producto = None
    finally:
        cursor.close()
        close_connection(conn)

    return render_template('check_product.html', producto=producto)  # Pasar el producto a la plantilla

# Inicio a la página de admin (productos)
@app.route('/admin')
def home():
    connection = create_connection()
    if connection:
        flash("Conexión exitosa a la base de datos")
        close_connection(connection)
    else:
        flash("Error al conectar a la base de datos")
    return render_template('admin/admin.html')

# Inicio a la página de usuarios
@app.route('/users')
def users():
    connection = create_connection()
    if connection:
        flash("Conexión exitosa a la base de datos")
        close_connection(connection)
    else:
        flash("Error al conectar a la base de datos")
    return render_template('admin/users.html')



@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT p.*, c.nombre AS categoriaNombre
        FROM producto p
        LEFT JOIN categoria c ON p.idCat = c.idCat
        """
        cursor.execute(query)
        productos = cursor.fetchall()
        print('Productos obtenidos:', productos)  # Log de los productos obtenidos
    except Exception as e:
        print('Error al obtener productos:', e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
    return jsonify(productos)

@app.route('/producto/data/<int:id>', methods=['GET'])
def obtener_producto(id):
    print(f'Request para obtener producto con ID: {id}')  # Log de solicitud
    conn = create_connection()
    if conn is None:
        print('Error de conexión a la base de datos')  # Log de error
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT p.*, c.nombre AS categoriaNombre FROM producto p LEFT JOIN categoria c ON p.idCat = c.idCat WHERE idProducto = %s", (id,))
        producto = cursor.fetchone()
        if producto:
            print('Producto encontrado:', producto)  # Log de producto encontrado
            return jsonify(producto)
        else:
            print('Producto no encontrado')  # Log de producto no encontrado
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        print('Error al obtener datos del producto:', e)  # Log para error
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_connection(conn)


@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 5))
        offset = (page - 1) * items_per_page
        search_query = request.args.get('query', '')

        # Construcción de la consulta con búsqueda y paginación
        query = """
        SELECT u.*
        FROM usuario u
        WHERE u.nombre LIKE %s OR u.email LIKE %s OR u.direccion LIKE %s
        OR u.telefono LIKE %s OR u.nombreRol LIKE %s
        LIMIT %s OFFSET %s
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (like_query, like_query, like_query, like_query, like_query, items_per_page, offset))
        usuarios = cursor.fetchall()

        # Consulta para obtener el total de usuarios sin paginación
        count_query = """
        SELECT COUNT(*) AS total
        FROM usuario
        WHERE nombre LIKE %s OR email LIKE %s OR direccion LIKE %s
        OR telefono LIKE %s OR nombreRol LIKE %s
        """
        cursor.execute(count_query, (like_query, like_query, like_query, like_query, like_query))
        total = cursor.fetchone()['total']

        return jsonify({'usuarios': usuarios, 'total': total})
    except Exception as e:
        print('Error al obtener usuarios:', e)
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


        

def actualizar_contrasenas_usuarios():
    usuarios = [
        {
            'email': 'admin1@gmail.com',
            'contrasena': 'miContraseñaAdmin',
            'rol': 'Administrador'
        },
        {
            'email': 'user1@gmail.com',
            'contrasena': 'miContraseña',
            'rol': 'Usuario'
        }
    ]
    
    connection = None
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        for usuario in usuarios:
            hashed_password = bcrypt.hashpw(usuario['contrasena'].encode('utf-8'), bcrypt.gensalt())
            
            # Actualiza la contraseña del usuario
            update_query = "UPDATE usuario SET contraseña = %s WHERE email = %s AND nombreRol = %s"
            cursor.execute(update_query, (hashed_password.decode('utf-8'), usuario['email'], usuario['rol']))
        
        connection.commit()
        print("Contraseñas de usuarios actualizadas con éxito.")
    
    except Exception as e:
        print(f"Error al actualizar las contraseñas de usuarios: {e}")
        if connection:
            connection.rollback()
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Llama a la función de actualización antes de iniciar la aplicación
actualizar_contrasenas_usuarios()

@app.route('/api/estado_sesion', methods=['GET'])
def estado_sesion():
    if 'user_id' in session:
        return jsonify({
            'usuarioLogueado': True,
            'idUsuario': session['user_id']
        })
    else:
        return jsonify({
            'usuarioLogueado': False,
            'idUsuario': None
        })
    

if __name__ == '__main__':
    print("Iniciando la aplicación...")
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")