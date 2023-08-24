from flask import Blueprint, render_template, request, flash, redirect,url_for
from products import get_products



client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/client/<username>', methods=['GET'])
def client_page(username):
    try:
        products_content = get_products()  
        return render_template('cliente.html', products=products_content, username=username)
    except Exception as ex:
        return {'error': str(ex)}, 500








