from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db import get_db_connection

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/login')
def show_login_page():
    return render_template('login.html')


@views_bp.route('/cliente.html')
def client_page():
    return render_template('cliente.html')