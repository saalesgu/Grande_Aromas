from flask import Blueprint, render_template, jsonify
from db import get_db_connection
from products import Products

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/admin')
def admin_page():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM products"
        cursor.execute(query)
        rows = cursor.fetchall()

        products_list = []
        for row in rows:
            product = Products(row[0], row[1], row[2], row[3], row[4], row[5])
            products_list.append(product.__dict__)

        cursor.close()
        connection.close()

        return render_template('admin.html', products=products_list)
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# Agrega más rutas y lógica para la administración aquí
