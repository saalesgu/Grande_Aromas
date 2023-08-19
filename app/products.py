from flask import Blueprint, jsonify, request, render_template, redirect, url_for
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

@products_bp.route('/create_product', methods=['POST'])
def create_product():
    if request.method == 'POST':
        data = request.json
        new_product = Products(
            product_name=data['product_name'],
            description=data['description'],
            quantity=data['quantity'],
            unit=data['unit'],
            price=data['price']
        )
        try:
            cursor = connection.cursor()
            query = "INSERT INTO products (product_name, description, quantity, unit, price) VALUES (%s, %s, %s, %s, %s)"
            values = (new_product.product_name, new_product.description, new_product.quantity, new_product.unit, new_product.price)
            cursor.execute(query, values)
            connection.commit()  # Confirmar los cambios en la base de datos
            cursor.close()
            connection.close()
            return jsonify({'message': 'Product created successfully'}), 201
        except Exception as ex:
            return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'message': 'Invalid method'}), 405

@products_bp.route('/get_products', methods=['GET'])
def get_products():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM products"
        cursor.execute(query)
        rows = cursor.fetchall()

        products_list = []
        for row in rows:
            product = Products(row[0], row[1], row[2], row[3], row[4], row[5])
            products_list.append(product.__dict__)

        cursor.close()
        return jsonify(products_list), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
