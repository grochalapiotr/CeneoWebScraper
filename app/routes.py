from app.models import Product
from app import app
from flask import render_template, redirect, url_for
from os import listdir

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html.jinja")

@app.route('/products')
def products():
    products = [x.split(".")[0] for x in listdir("app/products")]
    return render_template("products.html.jinja", products=products)

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.import_from_json()
    return render_template("product.html.jinja", product=str(product))

@app.route('/author')
def author():
    pass

@app.route('/extract/<product_id>')
def extract(product_id):
    product = Product(product_id)
    product.extract_opinions().analyze().export_to_json()
    return redirect(url_for('product', product_id=product_id))
    # return render_template("extract.html.jinja", product=str(product))