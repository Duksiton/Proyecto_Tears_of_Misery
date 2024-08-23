from flask import Flask, render_template, flash, jsonify
from mvc.model.db_connection import create_connection, close_connection
from mvc.controller.producto_controller import producto_controller

app = Flask(__name__)
app.secret_key = 'tearsofmiseryconexion'

# Registra el blueprint
app.register_blueprint(producto_controller)

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

if __name__ == '__main__':
    app.run(debug=True)
