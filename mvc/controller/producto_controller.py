#Importaciones
from flask import Blueprint, render_template, abort, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from mvc.model.db_connection import create_connection, close_connection

#Registro del blueprint producto_controller
producto_controller = Blueprint('producto_controller', __name__)

#Vista de productos
@producto_controller.route('/admin', methods=['GET'])
def admin():
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        abort(500, description="Error de conexión a la base de datos")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, c.nombre AS categoria 
            FROM producto p 
            JOIN categoria c ON p.idCat = c.idCat
        """)
        productos = cursor.fetchall()
        flash(f"Se obtuvieron {len(productos)} productos")
    except Exception as e:
        flash(f"Error al obtener productos: {str(e)}")
        productos = []
    finally:
        cursor.close()
        close_connection(conn)
    return render_template('admin/admin.html', productos=productos)

#Agregar producto
@producto_controller.route('/add_product', methods=['POST'])
def add_product():
    if 'imagen' not in request.files:
        flash("No se seleccionó una imagen")
        return redirect(url_for('producto_controller.admin'))
    
    imagen = request.files['imagen']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    idCat = int(request.form['idCat'])
    talla = request.form['talla']
    
    # Guardar imagen
    if imagen.filename == '':
        flash("No se seleccionó una imagen")
        return redirect(url_for('producto_controller.admin'))
    
    filename = secure_filename(imagen.filename)
    imagen_path = os.path.join('static/images', filename)
    imagen.save(imagen_path)
    
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        return redirect(url_for('producto_controller.admin'))
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO producto (nombre, descripcion, precio, stock, idCat, talla, imagen) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, descripcion, precio, stock, idCat, talla, filename))
        conn.commit()
        flash("Producto agregado exitosamente")
    except Exception as e:
        flash(f"Error al agregar el producto: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
    
    return redirect(url_for('producto_controller.admin'))


#Obtenemos el producto
@producto_controller.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM producto WHERE idProducto = %s", (id,))
        producto = cursor.fetchone()
        if producto:
            data = {
                'idProducto': producto[0],        # idProducto
                'nombre': producto[1],            # nombre
                'descripcion': producto[2],       # descripcion
                'precio': producto[4],            # precio
                'stock': producto[5],             # stock
                'imagen': producto[6]             # imagen
            }
            return jsonify(data)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_connection(conn)

#Un get para obtener los productos en modal
@producto_controller.route('/producto/<int:id>')
def get_producto(id):
    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE idProducto = %s", (id,))
        producto = cursor.fetchone()
        if producto:
            return jsonify(producto)
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        close_connection(conn)

#Actualizamos productos
@producto_controller.route('/update_product/<int:id>', methods=['POST'])
def update_product(id):
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        return redirect(url_for('producto_controller.admin'))

    try:
        cursor = conn.cursor()
        file = request.files.get('imagen')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        idCat = request.form.get('idCat')
        talla = request.form.get('talla')
        imagen_actual = request.form.get('imagenActual')

        # Primero, obtenemos la información actual del producto
        cursor.execute("SELECT imagen FROM producto WHERE idProducto = %s", (id,))
        producto_actual = cursor.fetchone()
        imagen_original = producto_actual[0] if producto_actual else None

        if file and file.filename:
            # Si se subió una nueva imagen, se usa esa
            filename = file.filename
        elif imagen_actual:
            # Si no se subió una nueva imagen pero hay una imagen actual, mantenemos esa
            filename = imagen_actual
        else:
            # Si no hay nueva imagen ni imagen actual, mantenemos la original
            filename = imagen_original

        print(f"Actualizando producto {id}. Imagen: {filename}")  # Log para depuración

        cursor.execute("""
            UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s, idCat = %s, talla = %s, imagen = %s
            WHERE idProducto = %s
        """, (nombre, descripcion, precio, stock, idCat, talla, filename, id))
        
        conn.commit()
        flash("Producto actualizado exitosamente")
    except Exception as e:
        print(f"Error al actualizar el producto: {str(e)}")  # Log para depuración
        flash(f"Error al actualizar el producto: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
    
    return redirect(url_for('producto_controller.admin'))

#Eliminamos productos
@producto_controller.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        return redirect(url_for('producto_controller.admin'))

    try:
        cursor = conn.cursor()

        # Primero obtenemos la imagen actual del producto para eliminarla si es necesario
        cursor.execute("SELECT imagen FROM producto WHERE idProducto = %s", (id,))
        producto = cursor.fetchone()

        if producto:
            imagen = producto[0]
            if imagen and imagen != "default.jpg":  # Verifica que la imagen no sea una predeterminada
                # Elimina la imagen del servidor
                os.remove(os.path.join('static', 'images', imagen))

            # Luego, eliminamos el producto de la base de datos
            cursor.execute("DELETE FROM producto WHERE idProducto = %s", (id,))
            conn.commit()
            flash("Producto eliminado exitosamente")
        else:
            flash("Producto no encontrado")

    except Exception as e:
        flash(f"Error al eliminar el producto: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)

    return redirect(url_for('producto_controller.admin'))
