from flask import Flask, render_template, request, redirect, url_for, session, flash ,jsonify 
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Asegúrate de definir una clave secreta segura

def conectar_db():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Ty321...',
        database='tearsOfMisery'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        contrasena = request.form.get('contrasena')
        connection = None
        try:
            connection = conectar_db()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM usuario WHERE email = %s AND contraseña = %s",
                (email, contrasena)
            )
            user = cursor.fetchone()
            if user:
                session['user'] = user
                return redirect(url_for('perfil'))  # Redirige a perfil.html
            else:
                flash("Credenciales incorrectas")
                return redirect(url_for('login'))
        except Error as e:
            flash(f"Error durante la conexión a la base de datos: {e}")
            return redirect(url_for('login'))
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        nombreRol = request.form['nombreRol']
        connection = None
        try:
            connection = conectar_db()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO usuario (nombre, email, contraseña, direccion, telefono, nombreRol) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, email, contrasena, direccion, telefono, nombreRol)
            )
            connection.commit()
            flash("Registro exitoso. Por favor, inicia sesión.")
            return redirect(url_for('login'))
        except Error as e:
            flash(f"Error durante la inserción: {e}")
            return redirect(url_for('registro'))
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('registro.html')

@app.route('/compra')
def compra():
    return render_template('compra.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    connection = conectar_db()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE usuario 
                SET nombre = %s, email = %s, direccion = %s, telefono = %s
                WHERE idUsuario = %s
            """, (nombre, email, direccion, telefono, user['idUsuario']))
            connection.commit()

            # Actualizar sesión con nuevos datos
            user['nombre'] = nombre
            user['email'] = email
            user['direccion'] = direccion
            user['telefono'] = telefono
            session['user'] = user

            flash("Perfil actualizado exitosamente.")
            return redirect(url_for('perfil'))

        except mysql.connector.Error as e:
            flash(f"Error al actualizar el perfil: {e}")
            return redirect(url_for('perfil'))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedido WHERE idUsuario = %s", (user['idUsuario'],))
    pedidos = cursor.fetchall()

    return render_template('perfil.html', user=user, pedidos=pedidos)

@app.route('/actualizar_perfil', methods=['POST'])
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
        conn = conectar_db()
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
    return redirect(url_for('perfil'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Eliminar el usuario de la sesión
    flash("Sesión cerrada exitosamente.")
    return redirect(url_for('login'))

@app.route('/comprar', methods=['POST'])
def comprar():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Lógica para manejar la compra
    return redirect(url_for('productos'))

@app.route('/comprar_todo', methods=['POST'])
def comprar_todo():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Lógica para manejar la compra de todo
    return redirect(url_for('productos'))

@app.route('/check_product')
def check_product():
    return render_template('check_product.html')

@app.route('/check_product2')
def check_product2():
    return render_template('check_product2.html')

@app.route('/check_product3')
def check_product3():
    return render_template('check_product3.html')

@app.route('/check_product4')
def check_product4():
    return render_template('check_product4.html')

@app.route('/check_product5')
def check_product5():
    return render_template('check_product5.html')

@app.route('/check_product6')
def check_product6():
    return render_template('check_product6.html')

@app.route('/check_product7')
def check_product7():
    return render_template('check_product7.html')

@app.route('/check_product8')
def check_product8():
    return render_template('check_product8.html')

if __name__ == '__main__':
    app.run(debug=True)
