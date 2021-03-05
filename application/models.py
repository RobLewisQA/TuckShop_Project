from application import db
from flask_table import Table, Col

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    customer_address = db.Column(db.String(100), nullable=True)
    customer_dob = db.Column(db.Date, nullable=False)
    prepaid_balance = db.Column(db.Float, nullable=False)
    orders=db.relationship('Orders',backref='customers')


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(30), nullable = False)
    product_brand = db.Column(db.String(30), nullable = True)
    quantity_in_stock = db.Column(db.Integer, nullable = False)
    cost_per_item = db.Column(db.Float, nullable = False)
    orders=db.relationship('Orders',backref='products')

class Orders(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    purchase_date=db.Column(db.Date,nullable=False)
    price=db.Column(db.Float,nullable=False)
    cash_payment=db.Column(db.Float,nullable=False)
    prepaid_payment = db.Column(db.Float,nullable=False)
    fk_customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=False)
    fk_product_id=db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)

########################

class ItemTable(Table):
    id = Col('product_id', show=False)
    product_name = Col('Product')
    product_brand = Col('Brand')
    quantity_in_stock = Col('Stock Available')
    cost_per_item = Col('item_cost',show=False)

class Item(object):
    def __init__(self, product_name, product_brand,quantity_in_stock):
        self.product_name = product_name
        self.product_brand = product_brand
        self.quantity_in_stock = quantity_in_stock
