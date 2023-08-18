from flask import Flask, render_template, request, jsonify
import psycopg2
from login import login_bp
from users import users_bp
from views import views_bp

try: 
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='Josari242008',
        database='Grande_Aromas'
    )
    print('Conexión exitosa')
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)

app = Flask(__name__)

# Registra el blueprint 'login'
app.register_blueprint(login_bp)
app.register_blueprint(users_bp)
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
