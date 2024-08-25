from flask import Flask, render_template, flash, jsonify
from mvc.model.db_connection import create_connection, close_connection
from mvc.controller.producto_controller import producto_controller
from mvc.controller.usuarios_controller import usuarios_controller


app = Flask(__name__)
app.secret_key = 'tearsofmiseryconexion'

# Registra el blueprint
app.register_blueprint(producto_controller)
app.register_blueprint(usuarios_controller)


@app.route('/')
def home():
    connection = create_connection()
    if connection:
        flash("Conexión exitosa a la base de datos")
        close_connection(connection)
    else:
        flash("Error al conectar a la base de datos")
    return render_template('admin/admin.html')

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
    # Consulta SQL actualizada para incluir el nombre de la categoría
    query = """
    SELECT p.*, c.nombre AS categoriaNombre
    FROM producto p
    LEFT JOIN categoria c ON p.idCat = c.idCat
    """
    cursor.execute(query)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(productos)


@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT * FROM usuario
    """
    cursor.execute(query)
    usuarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(usuarios)



if __name__ == '__main__':
    app.run(debug=True)
