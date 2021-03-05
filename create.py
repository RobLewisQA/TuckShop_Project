from application import db
from application.models import Customers,Products, Orders

db.create_all()

product_add = Products(product_name = 'Crunchie',product_brand="Cadbury's",quantity_in_stock = 10,cost_per_item = 0.20)
db.session.add(product_add)#Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p]))
db.session.commit()

#db.drop_all()
db.create_all()
p_names=['Aero','Dairy Milk','Twirl','Galaxy']
p_brands=['Nestle',"Cadbury's","Cadbury's",'Mars']
p_qtys=[10,10,10,10]
p_costs=[0.2,0.3,0.3,0.2]
p_list = []
#testuser = Users(first_name='Grooty',last_name='Toot') # Extra: this section populates the table with an example entry
for p in range(len(p_names)):
    #(Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p]))
#product_add = Products(product_name = 'Crunchie',product_brand="Cadbury's",quantity_in_stock = 10,cost_per_item = 0.20)
    db.session.add(Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p]))
db.session.commit()
