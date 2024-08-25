#Importaciones
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from mvc.model.db_connection import create_connection, close_connection

#Agregamos el blueprint de usuarios_controller
usuarios_controller = Blueprint('usuarios_controller', __name__)

#Listamos usuarios para su visualización 
@usuarios_controller.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        abort(500, description="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idUsuario, nombre, email, contraseña AS contrasena, direccion, telefono, nombreRol
            FROM usuario
        """)
        usuarios = cursor.fetchall()
        if not usuarios:
            flash("No se encontraron usuarios.")
        else:
            flash(f"Se obtuvieron {len(usuarios)} usuarios")
    except Exception as e:
        flash(f"Error al obtener usuarios: {str(e)}")
        usuarios = []
    finally:
        cursor.close()
        close_connection(conn)
    
    return render_template('admin/users.html', usuarios=usuarios)

#Obtenemos productos para organizarlos en listas
@usuarios_controller.route('/usuarios/<int:id>', methods=['GET'])
def get_user(id):
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre, email, contraseña AS contrasena, direccion, telefono, nombreRol
            FROM usuario
            WHERE idUsuario = %s
        """, (id,))
        user = cursor.fetchone()
        if user:
            user_data = {
                "nombre": user[0],
                "email": user[1],
                "contraseña": user[2],
                "direccion": user[3],
                "telefono": user[4],
                "nombreRol": user[5]
            }
            return jsonify(user_data)
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        print(f"Error al obtener el usuario: {str(e)}")
        return jsonify({"error": "Error al obtener el usuario"}), 500
    finally:
        cursor.close()
        close_connection(conn)

#Agregamos usuarios
@usuarios_controller.route('/usuarios/add', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        nombreRol = request.form['nombreRol']
        
        conn = create_connection()
        if conn is None:
            flash("Error de conexión a la base de datos")
            abort(500, description="Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuario (nombre, email, contraseña, direccion, telefono, nombreRol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, email, contraseña, direccion, telefono, nombreRol))
            conn.commit()
            flash("Usuario añadido con éxito")
            return redirect(url_for('usuarios_controller.listar_usuarios'))
        except Exception as e:
            flash(f"Error al añadir usuario: {str(e)}")
            conn.rollback()
        finally:
            cursor.close()
            close_connection(conn)
    
    return render_template('admin/add_user.html')

#Actualizamos usuarios
@usuarios_controller.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        return redirect(url_for('usuarios_controller.listar_usuarios'))

    try:
        cursor = conn.cursor()
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        nombreRol = request.form.get('nombreRol')
     
        cursor.execute("""
            UPDATE usuario SET nombre = %s, email = %s, contraseña = %s, direccion = %s, telefono = %s, nombreRol = %s
            WHERE idUsuario = %s
        """, (nombre, email, contraseña, direccion, telefono, nombreRol, id))
        
        conn.commit()
        flash("Usuario actualizado exitosamente")
    except Exception as e:
        print(f"Error al actualizar el usuario: {str(e)}")  # Log para depuración
        flash(f"Error al actualizar el usuario: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
    
    return redirect(url_for('usuarios_controller.listar_usuarios'))

#Eliminamos usuarios
@usuarios_controller.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        return redirect(url_for('usuarios_controller.listar_usuarios'))

    try:
        cursor = conn.cursor()

        # Eliminamos el usuario de la base de datos
        cursor.execute("DELETE FROM usuario WHERE idUsuario = %s", (id,))
        conn.commit()
        flash("Usuario eliminado exitosamente")
    except Exception as e:
        print(f"Error al eliminar el usuario: {str(e)}")  # Log para depuración
        flash(f"Error al eliminar el usuario: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)

    return redirect(url_for('usuarios_controller.listar_usuarios'))
