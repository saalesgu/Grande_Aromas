from flask import Flask, render_template, Blueprint

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/login')
def show_login_page():
    return render_template('login.html')

@views_bp.route('/admin.html')
def admin_page():
    return render_template('admin.html')

@views_bp.route('/cliente.html')
def client_page():
    return render_template('cliente.html')