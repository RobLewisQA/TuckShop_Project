from flask import url_for, redirect
from flask_testing import TestCase
from application import db, app, models
from application.models import Customers, Products, Orders
import sqlalchemy
import pandas as pd
from datetime import datetime

db.drop_all()
db.create_all()

# the code below adds data to the tables for testing
p_names=['Aero','Dairy Milk','Twirl','Galaxy']
p_brands=['Nestle',"Cadbury's","Cadbury's",'Mars']
p_qtys=[10,10,10,10]
p_costs=[0.2,0.3,0.3,0.2]
p_prices=[0.3,0.4,0.4,0.3]
p_list = []

for p in range(len(p_names)):
    db.session.add(Products(product_name = p_names[p],product_brand=p_brands[p],quantity_in_stock = p_qtys[p],cost_per_item = p_costs[p],price = p_prices[p]))
db.session.commit()

customer_add = Customers(first_name="John",last_name = "Doe",customer_address = '1 The Mall, London',customer_dob='2002-07-05')
db.session.add(customer_add)
customer_add2 = Customers(first_name="Jane",last_name = "Day",customer_address = '25 The Mall, London',customer_dob='1998-08-15')
db.session.add(customer_add2)
customer_add3 = Customers(first_name="Jorge",last_name = "Rodriguez",customer_address = '84 Privet Drive',customer_dob='1988-08-15')
db.session.add(customer_add3)
order_add = Orders(purchase_date = '2021-03-07',price=0.3,cash_payment = 0.3,quantity_ordered=1,fk_customer_id=1,fk_product_id=4)
db.session.add(order_add)
db.session.commit()

# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app
        app.config.update(SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@34.89.69.248/Tuckshop",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    def setUp(self):
        
        # Create tables
        db.create_all()
        db.session.commit()


#1. Home

class TestRoutes_general(TestBase):
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data != ''

class TestRoutes_create_read(TestBase):
    
    # add + read customer
    
    def test_add_customer(self):    # testing the customer addition form page
        response = self.client.get(url_for('add_customer'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
    
    def post_test_customer(self):   # testing the submission of a new customer
        self.client.post(url_for('add_customer'),data = dict(first_name='Charles',last_name='Tester',customer_address='10 Downing Street',customer_dob='1987-03-18',prepaid_balance= 0.00),follow_redirects=True)
        assert response.status_code == 200

    def test_add_customer_submission(self):    # testing the customer list page after submission for new entry 
        self.client.post(url_for('add_customers'),data = dict(first_name='Charles',last_name='Tester',customer_address='10 Downing Street',customer_dob='1987-03-18',prepaid_balance= 0.00),follow_redirects=True)
        response = self.client.get(url_for('read_customers'))
        self.assertIn(b"Tester",response.data)    
    
        # testing the rejection of duplicate addition 
        response1 = self.client.post(url_for('add_customers'),data = dict(first_name='Charles',last_name='Tester',customer_address='10 Downing Street',customer_dob='1987-03-18',prepaid_balance= 0.00),follow_redirects=True)
        self.assertIn(b"already exists",response1.data)


    # add + read product

    def test_add_product(self):    # testing the product addition form page
        response = self.client.get(url_for('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product Name", response.data)

    def post_test_product(self):    # testing the submission of a new product
        response1 = self.client.post(url_for('add_products'),data = dict(product_name='Snickers',product_brand='Mars',quantity_in_stock=10,cost_per_item=0.4,price= 0.55),follow_redirects=True)
        assert response1.status_code == 200
        self.assertIn(b"Snickers",response1.data)

    def post_test_product(self):    # testing the submission of a duplicate product
        self.client.post(url_for('add_products'),data = dict(product_name='Twirl',product_brand="Cadbury's",quantity_in_stock=10,cost_per_item=0.4,price= 0.55),follow_redirects=True)
        assert response1.status_code == 200
        response = self.client.get(url_for('read_products'))
        self.assertIn(b"Oops",response.data)

    def post_test_product_fail(self):    # testing the submission of a duplicate product for failure
        response1 = self.client.post(url_for('add_products'),data = dict(product_name='Aero',product_brand='Nestle',quantity_in_stock=10,cost_per_item=0.4,price= 0.55),follow_redirects=True)
        self.assertIn(b"Oops", response1.data)


    # add + read order

    def test_add_orders_formapage(self):    # testing the order addition form page 
        response = self.client.get(url_for('add_order'))
        assert response.status_code == 200
        date = datetime.today().strftime('%Y-%m-%d')
        assert str(date) in str(response.data)

    def test_add_order_submission(self):    # testing the submission of a new order and the order page after submission for new entry
        self.client.post(url_for('add_orders'),data = dict(date='2021-03-10',price=0.3,cash_payment=0.6,prepaid_payment=0,quantity_ordered=2,fk_customer_id= 1,fk_product_id=1),follow_redirects=True)
        response = self.client.get(url_for('read_orders'))
        self.assertIn(b"Aero",response.data)
        
    def test_products_post_order(self):    # testing the product list page after order submission for change in stock quantity  
        response1 = self.client.get(url_for('read_products'))
        df = pd.read_html(response1.data, header=0)[0]
        assert int(df.loc[df.Product == 'Aero'][['Quantity in stock']].sum()) == 8
    
    def test_failed_order_submission(self):    # testing the submission of an order with quantity-price-total mistake, and the order page after submission checking entry failed
        self.client.post(url_for('add_orders'),data = dict(date='2021-03-10',price=0.3,cash_payment=0.5,prepaid_payment=0,quantity_ordered=2,fk_customer_id= 3,fk_product_id=1),follow_redirects=True)
        response = self.client.get(url_for('read_orders'))
        self.assertNotIn(b"Rodriguez",response.data)
        response1 = self.client.get(url_for('read_products'))    # testing product stock quantities to validate order failure
        df = pd.read_html(response1.data, header=0)[0]
        assert int(df.loc[df.Product == 'Aero'][['Quantity in stock']].sum()) == 8

    def test_failed_order2_submission(self):    # testing the submission of an order with quantity-price-total mistake, and the order page after submission checking entry failed
        response1 = self.client.post(url_for('add_orders'),data = dict(date='2021-03-10',price=0.4,cash_payment=0.4,prepaid_payment=0,quantity_ordered=1,fk_customer_id= 3,fk_product_id=1),follow_redirects=True)
        self.assertIn(b"Oops",response1.data) 
        response = self.client.get(url_for('read_orders'))
        self.assertNotIn(b"Rodriguez",response.data)
        response2 = self.client.get(url_for('read_products'))    # testing product stock quantities to validate order failure
        df = pd.read_html(response2.data, header=0)[0]
        assert int(df.loc[df.Product == 'Aero'][['Quantity in stock']].sum()) == 8
    
    def test_failed_order3_submission(self):    # testing the submission of an order with quantity-price-total mistake, and the order page after submission checking entry failed
        response = self.client.post(url_for('add_orders'),data = dict(date='2021-03-10',price=0.3,cash_payment=8,prepaid_payment=0,quantity_ordered=20,fk_customer_id= 3,fk_product_id=1),follow_redirects=True)
        self.assertIn(b"Sorry",response.data) 
        response1 = self.client.get(url_for('read_products'))
        df = pd.read_html(response1.data, header=0)[0]
        df.columns = df.columns.str.replace(' ', '_',)
        assert int(df.loc[df.Product == "Aero"].Quantity_in_stock.sum()) == 8


    # update + read customer

class TestRoutes_update_read(TestBase):   
    def test_customer_update_submission(self):    # testing update of first name, last name, address, date of birth to customer record 2
        self.client.post('/customers/update/2',data = dict(id = 2, first_name='Joan',last_name='Sky',customer_address='4 Forkmoor Terrace',customer_dob='1988-08-15',prepaid_balance= 0.00),follow_redirects=True)
        self.client.post('/customers/update',data = dict(entry = 2, first_name='Joan',last_name='Sky',customer_address='4 Forkmoor Terrace',customer_dob='1988-08-15',prepaid_balance= 0.00),follow_redirects=True)
        response = self.client.get(url_for('read_customers'))
        self.assertIn(b"Joan",response.data)
        self.assertIn(b"1988-08-15",response.data)
        self.assertIn(b"Forkmoor",response.data)
        self.assertIn(b"Sky",response.data)
        
    def test_customer_update_page(self):    # testing the table in the update customers page to see that at least 1 record exists
        response = self.client.get(url_for('customer_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
        df = pd.read_html(response.data, header=0)[0]
        assert len(df) > 1


    # update + read product

    def test_products_update_submission(self):
        self.client.post('/products/update',data = dict(entry = 2, product_name='Chocolate Orange',product_brand="Terry's",quantity_in_stock=12,cost_per_item=0.5,price= 0.65),follow_redirects=True)
        response = self.client.get(url_for('products_update_page'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        self.assertIn(b"Chocolate Orange",response.data)
        self.assertIn(b"12",response.data)
        self.assertIn(b"Terry's",response.data)
        self.assertIn(b"0.5",response.data)
        self.assertIn(b"0.65",response.data)
    
    def product_update_form_page(self):
        response = self.client.get('/products/update/1',follow_redirects=True)
        self.assertIn(b"Aero",response.data)


    # update + read order

    def test_orders_update_page(self):    # testing order update form - incl. record table and prefilled values
        response = self.client.get(url_for('orders_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
        df = pd.read_html(response.data, header=0)[0]
        assert len(df) > 0

    def test_orders_update_subimission(self):    # testing successful order update submission        
        self.client.post('/orders/update',data = dict(entry = 1, purchase_date='2021-03-14',price=0.4,cash_payment=0.4,prepaid_payment=0.0,quantity_ordered=1,fk_customer_id= 3, fk_product_id=3),follow_redirects=True)
        response1 = self.client.get(url_for('orders_update_page'),follow_redirects=True)
        df1 = pd.read_html(response1.data, header=0)[0]
        assert response1.status_code == 200
        assert response1.data != ''

        response = self.client.get(url_for('read_orders'))    # testing order listings page for successful order amendment
        df2 = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        self.assertIn(b"Jorge",response.data)

    def test_update_order_sub2(self):
        self.client.post('/orders/update',data = dict(entry = 2, purchase_date='2021-03-14',price=0.3,cash_payment=1.2,prepaid_payment=0.0,quantity_ordered=4,fk_customer_id= 3, fk_product_id=1),follow_redirects=True)
        response = self.client.get(url_for('read_orders'))    # testing order listings page for successful order amendment
        df = pd.read_html(response.data, header=0)[0]
        self.assertIn(b"4",response.data)
        response2 = self.client.get(url_for('read_products'))
        df1 = pd.read_html(response2.data, header=0)[0]
        df1.columns = df1.columns.str.replace(' ', '_',)
        assert int(df1.loc[df1.Product == 'Aero'].Quantity_in_stock.sum()) == 6

    def test_orders_update_fail_1(self):    # testing update order failure due to wrong product-price pair
        response = self.client.post('/orders/update',data = dict(entry = 1, purchase_date='2021-03-14',price=0.4,cash_payment=0.4,prepaid_payment=0.0,quantity_ordered=1,fk_customer_id= 3, fk_product_id=1),follow_redirects=True)
        assert response.status_code == 200
        self.assertIn(b"Something",response.data)

    def test_orders_update_fail_1(self):    # testing update order failure due to wrong total_due-price-quantity trio
        response = self.client.post('/orders/update',data = dict(entry = 1, purchase_date='2021-03-14',price=0.4,cash_payment=0.4,prepaid_payment=0.0,quantity_ordered=1,fk_customer_id= 3, fk_product_id=1),follow_redirects=True)
        assert response.status_code == 200
        self.assertIn(b"Something",response.data)


class TestRoutes_delete_read(TestBase):    
    
    # delete + read customer

    def test_customers_delete(self):    # testing the deletion submission of a customer record
        response1 = self.client.get('/customers/delete/4',follow_redirects=True)
        self.assertEqual(response1.status_code, 200) 
        df = pd.read_html(response1.data, header=0)[0]            
        df.columns = df.columns.str.replace(' ', '_',)
        assert len(df.loc[df.Customer_ID == 4]) == 0


    # delete + read product

    def test_products_delete(self):    # testing the deletion submission of a product record
        response1 = self.client.post('/products/delete/2',follow_redirects=True)
        assert response1.status_code == 200
        response = self.client.get(url_for('read_products'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        df.columns = df.columns.str.replace(' ', '_',)
        assert len(df.loc[df.Product_ID == 2]) == 0

    def test_products_delete_fail(self):    # testing the deletion submission of a product record
        response = self.client.post('/products/delete/3',follow_redirects=True)
        self.assertIn(b"Oops",response.data)
        

    # delete + read order

    def test_orders_delete(self):    # testing the deletion of an order record - reading the order list and product list subsequently
        self.client.post('/orders/delete/2',follow_redirects=True)
        response = self.client.get(url_for('read_orders'),follow_redirects=True)
        df = pd.read_html(response.data, header=0)[0]
        assert response.status_code == 200
        assert response.data != ''
        df.columns = df.columns.str.replace(' ', '_',)
        assert len(df.loc[df.Order_ID == 2]) == 0

        response1 = self.client.get(url_for('read_products'),follow_redirects=True)
        df1 = pd.read_html(response1.data, header=0)[0]
        assert int(df1.loc[df1.Product == 'Aero'][['Quantity in stock']].sum()) == 10
