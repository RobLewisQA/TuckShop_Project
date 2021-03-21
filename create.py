from application import db
from application.models import Customers, Products, Orders
import pandas as pd

# drop and then create tables from scratch. All previous data is wiped, so this file should be run only to setup or restart the entire system
db.drop_all()
db.create_all()

# add test customer record
customer_add = Customers(first_name="Test_First_Name",last_name = "Test_Last_Name",customer_address = 'Test_Address',customer_dob='2002-07-05')
db.session.add(customer_add)

# add test product
db.session.add(Products(product_name = "Test_Product",product_brand="Test_Brand",quantity_in_stock = 100,cost_per_item = 1,price = 1))

# add test order
order_add = Orders(purchase_date = '1500-01-01',price=1,cash_payment = 1,quantity_ordered=1,fk_customer_id=1,fk_product_id=1)
db.session.add(order_add)

db.session.commit()
