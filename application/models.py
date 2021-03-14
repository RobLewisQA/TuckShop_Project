from application import db
from flask_table import Table, Col

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    customer_address = db.Column(db.String(50), nullable=True)
    customer_dob = db.Column(db.Date, nullable=False)
    prepaid_balance = db.Column(db.Float, nullable=True)
    orders=db.relationship('Orders',backref='customers')


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable = False)
    product_brand = db.Column(db.String(100), nullable = True)
    quantity_in_stock = db.Column(db.Integer, nullable = False)
    cost_per_item = db.Column(db.Float, nullable = False)
    price = db.Column(db.Float, nullable = False)
    #unique_itemname = db.Column(db.String, nullable = False)
    orders=db.relationship('Orders',backref='products')
    #prices=db.relationship('Orders',backref='prices')

class Orders(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    purchase_date=db.Column(db.Date,nullable=False)
    price=db.Column(db.Float,nullable=False)
    cash_payment=db.Column(db.Float,nullable=False)
    prepaid_payment = db.Column(db.Float,nullable=False)
    fk_customer_id=db.Column(db.Integer,db.ForeignKey('customers.id'),nullable=False)
    #fk_product_id = db.Column(db.Integer,nullable=False)
    fk_product_id=db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
    #fk_price = db.Column(db.Float,db.ForeignKey('prices.price'),nullable=False)
#########################

# class ItemTable(Table):
#     id = Col('product_id', show=False)
#     product_name = Col('Product')
#     product_brand = Col('Brand')
#     quantity_in_stock = Col('Stock Available')
#     cost_per_item = Col('item_cost',show=False)
#     price = Col('Price')

# class Item():
#     def __init__(self, product_name, product_brand,price,quantity_in_stock):
#         self.product_name = product_name
#         self.product_brand = product_brand
#         self.price = f"£ {price}"
#         self.quantity_in_stock = quantity_in_stock
#############
# class CustomersTable(Table):
#     id = Col('Customer ID', show=False)
#     first_name = Col('First Name')
#     last_name = Col('Surname')
#     customer_address = Col('Address')
#     prepaid_balance = Col('Prepaid Balance',show=False)
#     customer_dob = Col('Date of Birth')

# class Customer():
#     def __init__(self, first_name, last_name,customer_address,prepaid_balance,customer_dob):
#         #self.fk_price = fk_price
#         self.first_name = first_name
#         self.last_name = last_name
#         self.customer_address = customer_address
#         self.prepaid_balance = prepaid_balance
#         self.customer_dob = customer_dob
# #####################

# #####################
# class CustomersTable_checked(Table):
#     id = Col('Customer ID', show=False)
#     first_name = Col('First Name')
#     last_name = Col('Surname')
#     customer_address = Col('Address')
#     prepaid_balance = Col('Prepaid Balance',show=False)
#     customer_dob = Col('Date of Birth')
#     delete = Col('Delete')

# class Customer():
#     def __init__(self, first_name, last_name,customer_address,prepaid_balance,customer_dob,checked):
#         #self.fk_price = fk_price
#         self.first_name = first_name
#         self.last_name = last_name
#         self.customer_address = customer_address
#         self.prepaid_balance = prepaid_balance
#         self.customer_dob = customer_dob
#         self.delete = 'delete'
# #####################

# #####################
# class OrdersTable(Table):
#     id = Col('product_id', show=False)
#     purchase_date = Col('Date')
#     price = Col('Price')
#     cash_payment = Col('Value paid in cash')
#     prepaid_payment = Col('item_cost',show=False)
#     #fk_price = Col('Price')
#     fk_customer_id = Col('Customer Ref.')
#     fk_product_id = Col('Product Ref.')

# class Order(object):
#     def __init__(self, price, purchase_date,cash_payment,prepaid_payment,fk_customer_id,fk_product_id):
#         #self.fk_price = fk_price
#         self.price = price
#         self.purchase_date = purchase_date
#         self.cash_payment = cash_payment
#         self.prepaid_payment = prepaid_payment
#         self.fk_customer_id = fk_customer_id
#         self.fk_product_id = fk_product_id

# class OrdersSummary(Table):
#     id = Col('product_id', show=False)
#     first_name = Col('First Name')
#     surname = Col('Surname')
#     product = Col('Product')
#     brand = Col('Brand')
#     price = Col('Price')
#     purchase_date = Col('Date')
#     cash_payment = Col('Value paid in cash')
#     prepaid_payment = Col('item_cost',show=False)
#     #fk_price = Col('Price')
#     fk_customer_id = Col('Customer Ref.',show=False)
#     fk_product_id = Col('Product Ref.',show=False)

# class SummaryOrder(object):
#     def __init__(self, first_name, surname, product, brand,price, purchase_date,cash_payment,prepaid_payment,fk_customer_id,fk_product_id):
#         #self.fk_price = fk_price
#         self.first_name = first_name
#         self.surname = surname
#         self.product = product
#         self.brand = brand
#         self.price = price
#         self.purchase_date = purchase_date
#         self.cash_payment = cash_payment
#         self.prepaid_payment = prepaid_payment
#         self.fk_customer_id = fk_customer_id
#         self.fk_product_id = fk_product_id


