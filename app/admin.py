from flask import Blueprint, render_template, request, flash, redirect, url_for
from products import get_products, create_product
from db import get_db_connection


admin_bp = Blueprint('admin_bp', __name__ )

try:
    connection = get_db_connection()
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)


@admin_bp.route('/admin')
def admin_page():
    try:
        products_content = get_products()  
        return render_template('admin.html', products=products_content)
    except Exception as ex:
        return {'error': str(ex)}, 500
    
@admin_bp.route('/create_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            product_data = {
                'product_name': request.form.get('product_name'),
                'description': request.form.get('description'),
                'quantity': request.form.get('quantity'),
                'unit': request.form.get('unit'),
                'price': request.form.get('price')
            }
            print(product_data )
            result = create_product(product_data)

            if 'error' in result:
                flash('Error al crear el producto', 'danger')
            else:
                flash('Producto creado exitosamente', 'success')

        except Exception as ex:
            flash('Error al crear el producto', 'danger')
            print("Exception:", ex)  # Agrega esta línea para imprimir la excepción

        return redirect(url_for('admin_bp.admin_page'))

    elif request.method == 'GET':
        return render_template('create_product.html')

@admin_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        try:
            new_quantity = request.form.get('quantity')
            new_price = request.form.get('price')
            
            cursor = connection.cursor()
            query = "UPDATE products SET quantity = %s, price = %s WHERE id = %s"
            values = (new_quantity, new_price, product_id)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()

            flash('Producto actualizado exitosamente', 'success')

        except Exception as ex:
            flash('Error al actualizar el producto', 'danger')
            print("Exception:", ex)

        return redirect(url_for('products_bp.product_list'))
    
    elif request.method == 'GET':
        # Obtener los detalles del producto y renderizar la plantilla de edición
        # Puedes usar la misma idea que para mostrar los detalles del producto en la lista.
        return render_template('edit_product.html', product_id=product_id)

