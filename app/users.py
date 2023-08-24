from flask import Blueprint, jsonify, request, render_template,flash,redirect, url_for
from db import get_db_connection
from flask_login import UserMixin

users_bp = Blueprint('users_bp', __name__)

# Configura la conexión a la base de datos
try:
    connection = get_db_connection()
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)

class User(UserMixin):
    def __init__(self, id, rol_id, name, email, password):
        self.id = id
        self.rol_id = rol_id
        self.name = name
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True  # Cambia esto según la lógica de activación de tu usuario

    def is_authenticated(self):
        return True  # Cambia esto según la lógica de autenticación de tu usuario

    def is_anonymous(self):
        return False

@users_bp.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.json
        new_user = User(
            rol_id=data['rol_id'],
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (rol_id, name, email, password) VALUES (%s, %s, %s, %s)"
            values = (new_user.rol_id, new_user.name, new_user.email, new_user.password)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as ex:
            return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'message': 'Invalid method'}), 405


@users_bp.route('/get_users', methods=['GET'])
def get_users():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        rows = cursor.fetchall()

        users_list = []
        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4])
            users_list.append(user.__dict__)

        cursor.close()
        return jsonify(users_list), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@users_bp.route('/get_user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

        if row:
            user = {
                "id": row[0],
                "rol_id": row[1],
                "name": row[2],
                "email": row[3],
                "password": row[4],
            }
            cursor.close()
            connection.close()
            return jsonify(user), 200
        else:
            cursor.close()
            connection.close()
            return jsonify({'message': 'User not found'}), 404
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    
@users_bp.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        user_data = {
            'rol_id': 2,  
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (rol_id, name, email, password) VALUES (%s, %s, %s, %s)"
            values = (user_data['rol_id'], user_data['name'], user_data['email'], user_data['password'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('client_bp.client_page'))  
        except Exception as ex:
            return jsonify({'error': str(ex)}), 500
    else:
        return jsonify({'message': 'Invalid method'}), 405
    
@users_bp.route('/create_user_page', methods=['GET'])
def create_user_page():
    return render_template('create_account.html')

