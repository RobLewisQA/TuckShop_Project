from application import db
from flask_table import Table, Col

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    customer_address = db.Column(db.String(50), nullable=True)
    customer_dob = db.Column(db.Date, nullable=False)
    orders=db.relationship('Orders',backref='customers')


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable = False)
    product_brand = db.Column(db.String(100), nullable = True)
    quantity_in_stock = db.Column(db.Integer, nullable = False)
    cost_per_item = db.Column(db.Float, nullable = False)
    price = db.Column(db.Float, nullable = False)
    orders=db.relationship('Orders',backref='products')

class Orders(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    purchase_date=db.Column(db.Date,nullable=False)
    price=db.Column(db.Float,nullable=False)
    cash_payment=db.Column(db.Float,nullable=False)
    quantity_ordered = db.Column(db.Integer,nullable=False)
    fk_customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=False)
    fk_product_id=db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
