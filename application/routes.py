#from flask import Flask, redirect, request, url_for,render_template
from application import app, db
from application.models import Products,ItemTable


@app.route('/add')
def add():
    new_product = Products(product_name="Pepsi Max",product_brand="Pepsi",quantity_in_stock=5,cost_per_item=0.45)
    db.session.add(new_product)
    db.session.commit()
    return "Added new product to database"

@app.route('/products')
def read():
    items = Products.query.all()
    #all_products = Products.query.all()
    #products_string = ""
    #for product in all_products:
    #    products_string += "<br>"+ product.product_name 
    #return products_string
    table = ItemTable(items)
    return table.__html__()



@app.route('/update/<name>')
def update(name):
    first_product = Products.query.first()
    first_product.product_name = name
    db.session.commit()
    return first_product.product_name


'''
@app.route('/')

def hello_internet():
    return "Hello internet"

@app.route('/users/<name>/<int:id>')
def users(name,id):
    return f"Hello, {name}, your ID is {id}"

'''