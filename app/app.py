from flask import Flask, render_template, request, jsonify
from login import login_bp
from users import users_bp
from views import views_bp
from products import products_bp
from db import get_db_connection
from admin import admin_bp



try: 
    connection = get_db_connection()
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)

app = Flask(__name__)

# Registra el blueprint 'login'
app.register_blueprint(login_bp)
app.register_blueprint(users_bp)
app.register_blueprint(views_bp)
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
