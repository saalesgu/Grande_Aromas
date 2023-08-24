from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from db import get_db_connection


products_bp = Blueprint('products_bp', __name__)

try:
    connection = get_db_connection()
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)

class Products:
    def __init__(self, id, product_name, description, quantity, unit, price):
        self.id = id
        self.product_name = product_name
        self.description = description
        self.quantity = quantity
        self.unit = unit
        self.price = price

from flask import flash, redirect, url_for

#@products_bp.route('/create_product', methods=['POST'])
def create_product(new_product):
    if request.method == 'POST':
        try:
            new_product = {
                'product_name': request.form.get('product_name'),
                'description': request.form.get('description'),
                'quantity': request.form.get('quantity'),
                'unit': request.form.get('unit'),
                'price': request.form.get('price')
            }
            
            cursor = connection.cursor()
            query = "INSERT INTO products (product_name, description, quantity, unit, price) VALUES (%s, %s, %s, %s, %s)"
            values = (new_product['product_name'], new_product['description'], new_product['quantity'], new_product['unit'], new_product['price'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()

            flash('Producto creado exitosamente', 'success') 
              
        except Exception as ex:
            print("Exception:", ex)  
            return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'message': 'Invalid method'}), 405



@products_bp.route('/get_products', methods=['GET'])
def get_products():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM products"
        cursor.execute(query)
        rows = cursor.fetchall()

        products_list = []
        for row in rows:
            product = {
                "id": row[0],
                "product_name": row[1],
                "description": row[2],
                "quantity": row[3],
                "unit": row[4],
                "price": row[5]
            }
            products_list.append(product)

        cursor.close()
        connection.close()

        return products_list  
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@products_bp.route('/get_product/<int:product_id>', methods=['GET'])
def get_product_id(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        if row:
            product = {
                "id": row[0],
                "product_name": row[1],
                "description": row[2],
                "quantity": row[3],
                "unit": row[4],
                "price": row[5]
            }
            cursor.close()
            connection.close()
            return jsonify(product), 200
        else:
            cursor.close()
            connection.close()
            return jsonify({'message': 'Product not found'}), 404
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

