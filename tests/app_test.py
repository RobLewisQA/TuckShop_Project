from flask import url_for, redirect
from flask_testing import TestCase
from application import db, app, models
import sqlalchemy
import pandas as pd


# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@34.89.69.248/Tuckshop",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    def setUp(self):
        # Create tables
        db.create_all()
        #p_names=['Aero','Dairy Milk','Twirl','Galaxy']
        #p_brands=['Nestle',"Cadbury's","Cadbury's",'Mars']
        #p_qtys=[10,10,9,9]
        #p_costs=[0.2,0.3,0.3,0.2]
        #p_prices=[0.3,0.4,0.4,0.3]
        ##p_list = []
        #for p in range(len(p_names)):
        #    db.session.add(models.Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p],price = p_prices[p]))
        #customer_add = models.Customers(first_name="John",last_name = "Doe",customer_address = '1 The Mall, London',customer_dob='2020-07-05',prepaid_balance=0)
        #db.session.add(customer_add)
        db.session.commit()

    def tearDown(self):
        statement=""
        db.session.commit()
        #db.session.remove()
        #db.drop_all()


###################      class1:test add+read, class2:test update+read, class3:test delete+read      ######################


#1. Home
class TestRoutes_general(TestBase):
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data != ''
    def test_customer_(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data != ''

class TestRoutes_create_read(TestBase):
    ####### add + read customer
    def test_add_customer(self):
        response = self.client.get(url_for('add_customer'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
    def post_test_customer(self):
        self.client.post(url_for('add_customer'),data = dict(first_name='Charles',last_name='Tester',customer_address='10 Downing Street',customer_dob='1987-03-18',prepaid_balance= 0.00),follow_redirects=True)
        assert response.status_code == 200
    def test_add_customer_submission(self):
        self.client.post(url_for('add_customers'),data = dict(first_name='Charles',last_name='Tester',customer_address='10 Downing Street',customer_dob='1987-03-18',prepaid_balance= 0.00),follow_redirects=True)
        response = self.client.get(url_for('read_customers'))
        self.assertIn(b"Tester",response.data)    

    ####### add + read product
    def test_add_product(self):
        response = self.client.get(url_for('add_product'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
    def post_test_product(self):
        self.client.post(url_for('add_product'),data = dict(product_name='Snickers',product_brand='Mars',quantity_in_stock=10,cost_per_item=0.4,price= 0.55),follow_redirects=True)
        assert response.status_code == 200
        response = self.client.get(url_for('read_products'))
        self.assertIn(b"Snickers",response.data)
    def test_add_product_submission(self):
        response = self.client.get(url_for('add_products'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''

    ####### add + read order
    def test_add_orders_formapage(self):
        response = self.client.get(url_for('add_order'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
    def test_add_order_submission(self):
        self.client.post(url_for('add_orders'),data = dict(date='2021-03-10',price=0.3,cash_payment=0.3,prepaid_payment=0,quantity_ordered=2,fk_customer_id= 1,fk_product_id=1),follow_redirects=True)
        response = self.client.get(url_for('read_orders'))
        self.assertIn(b"Aero",response.data)
        
        response1 = self.client.get(url_for('read_products'))
        df = pd.read_html(response1.data, header=0)[0]
        assert (df.loc[df.product_name == 'Aero'].quantity_in_stock).sum() == 8

class TestRoutes_update_read(TestBase):   
    ####### update + read customer
    def test_customer_update_submission(self):
        self.client.post('/customers/update/2',data = dict(id = 2, first_name='Joan',last_name='Day',customer_address='4 Forkmoor Terrace',customer_dob='1988-08-15',prepaid_balance= 0.00),follow_redirects=True)
        self.client.post('/customers/update',data = dict(entry = 2, first_name='Joan',last_name='Day',customer_address='4 Forkmoor Terrace',customer_dob='1988-08-15',prepaid_balance= 0.00),follow_redirects=True)
        response = self.client.get(url_for('read_customers'))
        self.assertIn(b"Joan",response.data)
    def test_customer_update_page(self):
        response = self.client.get(url_for('customer_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
        df = pd.read_html(response.data, header=0)[0]
        assert len(df) > 1
    ####### update + read product
    def test_products_update_submission(self):
        self.client.post('/products/update',data = dict(entry = 1, product_name='KitKat',product_brand='Nestle',quantity_in_stock=10,cost_per_item=0.4,price= 0.65),follow_redirects=True)
        response = self.client.get(url_for('products_update_page'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        self.assertIn(b"KitKat",response.data)
    ####### update + read order
    def test_orders_update_page(self):
        response = self.client.get(url_for('orders_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
        df = pd.read_html(response.data, header=0)[0]
        assert len(df) > 0
    
    def test_orders_update_subimission(self):
        self.client.post('/orders/update',data = dict(entry = 1, purchase_date='2021-03-14',price=0.4,cash_payment=0.4,prepaid_payment=0.0,quantity_ordered=1,fk_customer_id= 3, fk_product_id=3),follow_redirects=True)
        #self.client.post('/orders/update',follow_redirects=True)
        response = self.client.get(url_for('read_orders'))
        df2 = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        self.assertIn(b"Jorge",response.data)

class TestRoutes_delete_read(TestBase):    
    ####### delete + read customer
    def test_customers_delete(self):   
        self.client.post('/customers/delete/4',follow_redirects=True)
        response = self.client.get(url_for('read_customers'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        assert len(df.loc[df.id == 4]) == 0

    ####### delete + read product
    def test_products_delete(self):
        self.client.post('/products/delete/2',follow_redirects=True)
        response = self.client.get(url_for('read_products'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        assert len(df.loc[df.id == 2]) == 0

    ####### delete + read order
    def test_orders_delete(self):   
        self.client.post('/orders/delete/2',follow_redirects=True)
        response = self.client.get(url_for('read_orders'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        assert len(df.loc[df.id_x == 2]) == 0



























        
# ##a. add customers - test page response, return template, redirect, post
# '''
#         #df = pd.read_html(response.data, header=0)[0]
#         #df.loc[df.product_name == 'Aero'].quantity_in_stock == 9
# ##b. read customers - test page response, links
#     def test_read_customers(self):
#         response = self.client.get(url_for('read_customers'),follow_redirects=True)
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         assert len(df) >= 1
# ##c.update customers - test update page response, table, links
#     def test_customer_update_submission(self):
#         self.client.post('/customers/update/2',data = dict(first_name='Joan',last_name='Day',customer_address='4 Forkmoor Terrace',customer_dob='1988-08-15',prepaid_balance= 0.00),follow_redirects=True)
#         #response = self.client.get(url_for('read_customers'))
#         #self.assertIn(b"Joan",response.data)
# ##c. update customers2 - test form response, table view, post
#     def test_customer_update_page(self):
#         response = self.client.get(url_for('customer_update_page'),follow_redirects=True)
#         assert response.status_code == 200
#         assert response.data != ''
# ##d. delete customers - test page response, redirect, deletion of record(s)
#     def test_customers_delete(self):   
#         self.client.post('/customers/delete/3',follow_redirects=True)
#         response = self.client.get(url_for('read_customers'),follow_redirects=True)
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         assert len(df.loc[df.id == 3]) == 0

#     '''###########################################
#     #3. Products
#     ''' ''''''''''''''''''''''''''''''''''''''''''
# ##a. add products - test page response, return template, redirect, post
    
    
# ##b. read products - test page response, links
#     def test_read_products(self):
#         response = self.client.get(url_for('read_products'))
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         assert len(df) >= 1
#         #self.assertIn(b"Twix",response.data)
# ##c.update products - test update page response, table, links

# ##c. update products2 - test form response, table view, post
#     def test_products_update_page(self):
#         response = self.client.get(url_for('products_update_page'),follow_redirects=True)
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         assert len(df) >= 1
# ##d. delete products - test page response, redirect, deletion of record(s)
#     def test_products_delete(self):
#         self.client.post('/products/delete/2',follow_redirects=True)
#         response = self.client.get(url_for('read_products'),follow_redirects=True)
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         assert len(df.loc[df.id == 2]) == 0

#     '''###########################################
#     #4. Orders
#     ''' ''''''''''''''''''''''''''''''''''''''''''
# ##a. add orders - test page response, return template, redirect, post
#     def test_add_orders_formapage(self):
#         response = self.client.get(url_for('add_order'),follow_redirects=True)
#         assert response.status_code == 200
#         assert response.data != ''
#     def test_add_order_submission(self):
#         self.client.post(url_for('add_orders'),data = dict(date='2021-03-10',price=0.3,cash_payment=0.3,prepaid_payment=0,fk_customer_id= 1,fk_product_id=1),follow_redirects=True)
#         response = self.client.get(url_for('read_orders'))
#         self.assertIn(b"Aero",response.data)
        
#         response1 = self.client.get(url_for('read_products'))
#         df = pd.read_html(response1.data, header=0)[0]
#         assert (df.loc[df.product_name == 'Aero'].quantity_in_stock).sum() == 9
    
#     #def test_add_order_sub(self):
#         #self.client.post(url_for('add_order'),data = dict(date='2021-03-10',price=0.3,cash_payment=0.3,prepaid_payment=0,fk_customer_id= 1,fk_product_id=1),follow_redirects=True)
#         #response = self.client.get(url_for('add_order'))
#         #df = pd.read_html(response.data, header=0)[0]
#         #assert len(df) >= 1

#         #response = self.client.get(url_for('read_orders'))
#         #self.assertIn(b"Twirl",response.data)
#     #def test_add_order_listing(self):
#     #    response = self.client.get(url_for('read_orders'))
#     #    self.assertIn(b"Twirl",response.data)

#     def test_add_order_stock(self):
#         response = self.client.get(url_for('read_products'))
#         df = pd.read_html(response.data, header=0)[0]
#         assert df.loc[df.product_name == 'Aero'].quantity_in_stock.sum() == 9

#         #self.assertIn(b"Aero",response.data)
#         #self.assertIn(b"8",response.data)

#         #self.assertIn(b"Cadbury's",response.data)
#         #assert models.Products.query(products_name="Dairy Milk").with_entities(Products.quantity_in_stock).all() == 9

#     def test_read_neworder(self):
#         response = self.client.get(url_for('read_orders'))
#         #self.assertIn(b"Cadbury's",response.data)
#     #def test_posted_order(self):
#     #    response2 = self.client.get(url_for('read_orders')
#     #    self.assertIn(b"Cadbury's",response2.data)

# ##b. read orders - test page response, links
#     def test_read_orders(self):
#         response = self.client.get(url_for('read_orders'),follow_redirects=True)
#         assert response.status_code == 200
#         assert response.data != ''
# ##c.update orders - test update page response, table, links
#     def test_orders_update_subimission(self):
#         self.client.post('/orders/update/2',data = dict(date='2021-03-10',price=0.3,cash_payment=0.3,prepaid_payment=0,fk_customer_id= 2,fk_product_id=1),follow_redirects=True)
#         response = self.client.get(url_for('read_orders'),follow_redirects=True)
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         print(df.loc[df.id_x == 1].first_name)
#         assert df.loc[df.id_x == 1].first_name == 'Jane'
#         #assert response.status_code == 200
#         #assert response.data != ''

#     #def test_orders_update_subimission(self):
#     #    response = self.client.get(url_for('order_update1'),follow_redirects=True)
#     #    assert response.status_code == 200
#     #    assert response.data != ''

# ##c. update orders2 - test form response, table view, post
#     def test_orders_update_page(self):
#         response = self.client.get(url_for('orders_update_page'),follow_redirects=True)
#         assert response.status_code == 200
#         assert response.data != ''
        
# ##d. delete orders - test page response, redirect, deletion of record(s)
#     def test_orders_delete(self):   
#         self.client.post('/orders/delete/1',follow_redirects=True)
#         response = self.client.get(url_for('read_orders'),follow_redirects=True)
#         df = pd.read_html(response.data, header=0)[0]
#         assert response.status_code == 200
#         assert response.data != ''
#         assert len(df.loc[df.id_x == 1]) == 0

# '''