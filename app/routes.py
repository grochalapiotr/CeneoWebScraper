from app.models import Product
from app import app
from flask import render_template, redirect, url_for, request
from os import listdir

#@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/products')
def products():
    products_names={}
    products = [x.split(".")[0] for x in listdir("app/products")]
    for product_id in products:
        product = Product(product_id)
        product.import_from_json()
        product = product.to_dict()
        products_names[product_id]=product['product_name']
    return render_template("products.html.jinja", products=products, products_names=products_names)

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.import_from_json()
    return render_template("product.html.jinja", product=product.to_dict())

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product(product_id)
        product.extract_name()
        if product.product_name is None:
            return render_template("extract.html.jinja", error="Podana wartość nie jest poprawnym kodem produktu")
        else:
            product.extract_opinions().analyze().export_to_json()
            return redirect(url_for('product', product_id=product_id))
    return render_template("extract.html.jinja")