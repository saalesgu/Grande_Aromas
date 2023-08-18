from flask import Blueprint, jsonify, request, render_template
import psycopg2  # Importa la librería para la conexión con la base de datos

users_bp = Blueprint('users_bp', __name__)

# Configura la conexión a la base de datos
try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='Josari242008',
        database='Grande_Aromas'
    )
    print('Conexión a la base de datos exitosa')
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)

class User:
    def __init__(self,rol_id, name, email, password):
        self.rol_id = rol_id
        self.name = name
        self.email = email
        self.password = password

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