from flask import Blueprint, jsonify, request, render_template, redirect, url_for
import psycopg2

login_bp = Blueprint('login_bp', __name__)

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

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_data = valid_login(email, password)
        if user_data is not None:
            rol_id = user_data[1]

            if rol_id == 2:
                return redirect(url_for('views.admin_page'))
            elif rol_id == 1:
                return redirect(url_for('views.client_page'))
            else:
                return jsonify({'error': 'Unknown role'}), 401
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return render_template('login.html')

def valid_login(email, password):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        user_data = cursor.fetchone()
        cursor.close()
        return user_data
    except Exception as ex:
        print('Error:', ex)
        return None
