from flask import Flask
from login import login_bp, login_manager
from users import users_bp
from views import views_bp
from products import products_bp
from db import get_db_connection
from admin import admin_bp
from client import client_bp
from flask_login import current_user


try: 
    connection = get_db_connection()
except Exception as ex:
    print('Error al conectar a la base de datos:', ex)

app = Flask(__name__)
app.secret_key = 'GrandeAromas123'


app.register_blueprint(login_bp)
app.register_blueprint(users_bp)
app.register_blueprint(views_bp)
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)


@app.context_processor
def inject_user():
    return dict(current_user=current_user)

login_manager.init_app(app)  # Donde "app" es tu objeto Flask

if __name__ == '__main__':
    app.run(debug=True, port=5000)
