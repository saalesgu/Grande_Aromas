from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from db import get_db_connection
from users import User


login_bp = Blueprint('login_bp', __name__)
login_manager = LoginManager()

try:
    connection = get_db_connection()
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
            if rol_id == 1:
                return redirect(url_for('admin_bp.admin_page'))
            elif rol_id == 2:
                username = user_data[2]  
                return redirect(url_for('client_bp.client_page', username=username))
            else:
                return jsonify({'error': 'Unknown role'}), 401
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return render_template('login.html')

@login_bp.route('/logout')
def logout():
    logout_user()
    print("Usuario desconectado")
    return redirect(url_for('views.index'))

def valid_login(email, password):
    try:
        cursor = connection.cursor()
        query = "SELECT id, rol_id, name, email, password FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        user_data = cursor.fetchone()
        cursor.close()
        return user_data
    except Exception as ex:
        print('Error:', ex)
        return None


@login_bp.route('/get_current_user_id', methods=['GET'])
def get_current_user_id():
    try:
        if current_user.is_authenticated:
            return jsonify({'user_id': current_user.get_id()})
        else:
            return jsonify({'user_id': None})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    

@login_manager.user_loader
def load_user(id):
    try:
        cursor = connection.cursor()
        query = "SELECT id, rol_id, name, email, password FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            id, rol_id, name, email, password = user_data
            
            return User(id, rol_id, name, email, password)
        else:
            return None
    except Exception as ex:
        print('Error:', ex)
        return None