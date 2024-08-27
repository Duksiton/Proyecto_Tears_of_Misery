# Importaciones
from flask import Flask, render_template, flash, jsonify, request, redirect, url_for
from mvc.model.db_connection import create_connection, close_connection
from mvc.controller.producto_controller import producto_controller
from mvc.controller.usuarios_controller import usuarios_controller
from mvc.controller.login_controller import login_controller
from mvc.controller.registro_controller import registro_controller
from mvc.controller.perfil_controller import perfil_controller
from mvc.controller.logout_controller import logout_controller

app = Flask(__name__)
app.secret_key = 'tearsofmiseryconexion'

# Registro de los blueprints
app.register_blueprint(producto_controller)
app.register_blueprint(usuarios_controller)
app.register_blueprint(login_controller)
app.register_blueprint(registro_controller)
app.register_blueprint(perfil_controller)
app.register_blueprint(logout_controller)

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


if __name__ == '__main__':
    print("Iniciando la aplicación...")
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")