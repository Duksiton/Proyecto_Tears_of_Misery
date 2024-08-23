from flask import Blueprint, render_template, abort, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from mvc.model.db_connection import create_connection, close_connection


producto_controller = Blueprint('producto_controller', __name__)

@producto_controller.route('/admin', methods=['GET'])
def admin():
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        abort(500, description="Error de conexión a la base de datos")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, c.nombre AS categoria_nombre 
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
               'imagen': producto[0],        
                'productoId': producto[6],       
                'nombre': producto[1],         
                'descripcion': producto[2],    
                'precio': producto[4],         
                'stock': producto[5],          
                'idCat': producto[6],          
                'talla': producto[7]           
            }
            return jsonify(data)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        close_connection(conn)

@producto_controller.route('/update_product/<int:id>', methods=['POST'])
def update_product(id):
    conn = create_connection()
    if conn is None:
        flash("Error de conexión a la base de datos")
        return redirect(url_for('producto_controller.admin'))

    try:
        cursor = conn.cursor()
        filename = request.files.get('imagen')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        idCat = request.form.get('idCat')
        talla = request.form.get('talla')
        
        if filename and filename.filename:
            filename = filename.filename
            cursor.execute("""
                UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s, idCat = %s, talla = %s, imagen = %s
                WHERE idProducto = %s
            """, (nombre, descripcion, precio, stock, idCat, talla, filename, id))
        else:
            # Si no se sube una nueva imagen, se debe mantener la imagen actual
            current_image = request.form.get('imagenActual')
            cursor.execute("""
                UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s, idCat = %s, talla = %s, imagen = %s
                WHERE idProducto = %s
            """, (nombre, descripcion, precio, stock, idCat, talla, current_image, id))
        
        conn.commit()
        flash("Producto actualizado exitosamente")
    except Exception as e:
        flash(f"Error al actualizar el producto: {str(e)}")
    finally:
        cursor.close()
        close_connection(conn)
    
    return redirect(url_for('producto_controller.admin'))


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
                os.remove(os.path.join('/path/to/uploaded/images/', imagen))

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
