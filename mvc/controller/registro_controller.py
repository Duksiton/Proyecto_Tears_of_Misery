from flask import Blueprint, render_template, request, redirect, url_for, flash
from mvc.model.db_connection import create_connection, close_connection
from mysql.connector import Error

registro_controller = Blueprint('registro_controller', __name__)

@registro_controller.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        connection = None
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO usuario (nombre, email, contraseña) VALUES (%s, %s, %s)",
                (nombre, email, contrasena)
            )
            connection.commit()
            flash("Usuario registrado con éxito. Por favor, inicia sesión.")  # Mensaje de éxito
            return redirect(url_for('login_controller.login'))  # Usar el blueprint y endpoint correcto
        except Error as e:
            flash(f"Error durante la inserción: {e}")  # Mensaje de error
            return redirect(url_for('registro_controller.registro'))  # Usar el blueprint y endpoint correcto
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('registro.html')
