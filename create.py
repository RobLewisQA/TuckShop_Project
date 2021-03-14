from application import db
from application.models import Customers, Products, Orders
import pandas as pd

#product_add = Products(product_name = 'Crunchie',product_brand="Cadbury's",quantity_in_stock = 10,cost_per_item = 0.20)
#db.session.add(product_add)#Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p]))
#db.session.commit()
db.drop_all()
db.create_all()
p_names=['Aero','Dairy Milk','Twirl','Galaxy']
p_brands=['Nestle',"Cadbury's","Cadbury's",'Mars']
p_qtys=[10,10,10,10]
p_costs=[0.2,0.3,0.3,0.2]
p_prices=[0.3,0.4,0.4,0.3]
p_list = []
#testuser = Users(first_name='Grooty',last_name='Toot') # Extra: this section populates the table with an example entry
for p in range(len(p_names)):
    #(Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p]))
#product_add = Products(product_name = 'Crunchie',product_brand="Cadbury's",quantity_in_stock = 10,cost_per_item = 0.20)
    db.session.add(Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p],price = p_prices[p]))
db.session.commit()

customer_add = Customers(first_name="John",last_name = "Doe",customer_address = '1 The Mall, London',customer_dob='2002-07-05',prepaid_balance=0)
db.session.add(customer_add)
customer_add2 = Customers(first_name="Jane",last_name = "Day",customer_address = '25 The Mall, London',customer_dob='1998-08-15',prepaid_balance=0)
db.session.add(customer_add2)
customer_add3 = Customers(first_name="Jorge",last_name = "Rodriguez",customer_address = '84 Privet Drive',customer_dob='1988-08-15',prepaid_balance=0)
db.session.add(customer_add3)
order_add = Orders(purchase_date = '2021-03-07',price=0.3,cash_payment = 0.3,prepaid_payment = 0,fk_customer_id=1,fk_product_id=4)
db.session.add(order_add)
#db.session.add(Customers(first_name="John",last_name = "Doe",customer_address = '1 The Mall, London',customer_dob='2020-07-05'))
db.session.commit()
#db.drop_all()
'''
order_add = Orders(purchase_date = '2021-03-07',price=0.3,cash_payment = 0.3,prepaid_payment = 0,fk_customer_id=1,fk_product_id=4)
db.session.add(order_add)
db.session.commit()

order_add = Orders(purchase_date = '2021-03-08',price=0.4,cash_payment = 0.4,prepaid_payment = 0,fk_customer_id=1,fk_product_id=3)
db.session.add(order_add)
db.session.commit()
'''

