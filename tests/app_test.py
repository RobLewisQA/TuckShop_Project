from flask import url_for
from flask_testing import TestCase
from application import db, app

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
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

#class TestViews(TestBase):
#    def test_home_get(self):
#        response = self.client.get(url_for('home'))
#        self.assertEqual(response.status_code, 200)

#1. Home
class TestRoutes(TestBase):
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data != ''


    '''###########################################
    #2. Customers
     '''''''''''''''''''''''''''''''''''''''''''''
##a. add customers - test page response, return template, redirect, post
    def test_add_customer(self):
        response = self.client.get(url_for('add_customer'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
#def test_home_redir():
#    response = app.test_client().get('/home')
#    assert response.status_code == 200
#    assert response.data != ''

##b. read customers - test page response, links
    def test_read_customers(self):
        response = self.client.get(url_for('read_customers'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
##c.update customers - test update page response, table, links
##c. update customers2 - test form response, table view, post
    def test_customer_update_page(self):
        response = self.client.get(url_for('customer_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
##d. delete customers - test page response, redirect, deletion of record(s)


    '''###########################################
    #3. Products
    ''' ''''''''''''''''''''''''''''''''''''''''''
##a. add products - test page response, return template, redirect, post
    def test_add_products(self):
        response = self.client.get(url_for('add_item'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
    def post_test_product(self):
        response1 = self.client.post(url_for('add_order'),data = dict(product_namee='Twix',product_brand='Mars',quantity_in_stock=11,cost_per_item=0.35,price=0.5),follow_redirects=True)
        assert response1.data != ""
        self.assertIn(b"Twix",response1.data)
        self.assertIn(b"11",response1.data)
##b. read products - test page response, links
    def test_read_products(self):
        response = self.client.get(url_for('read_products'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
##c.update products - test update page response, table, links
##c. update products2 - test form response, table view, post
    def test_products_update_page(self):
        response = self.client.get(url_for('products_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
##d. delete products - test page response, redirect, deletion of record(s)


    '''###########################################
    #4. Orders
    ''' ''''''''''''''''''''''''''''''''''''''''''
##a. add orders - test page response, return template, redirect, post
    def test_add_orders(self):
        response = self.client.get(url_for('add_order'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
    def post_test_order(self):
        response1 = self.client.post(url_for('add_order'),data = dict(purchase_date='2021-03-10',price=0.4,cash_payment=0.4,prepaid_payment=0,fk_customer_id= 1,fk_product_id=2),follow_redirects=True)
        assert response1.data != ""
        self.assertIn(b"Cadbury's",response1.data)
##b. read orders - test page response, links
    def test_read_orders(self):
        response = self.client.get(url_for('read_orders'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
##c.update orders - test update page response, table, links
##c. update orders2 - test form response, table view, post
    def test_orders_update_page(self):
        response = self.client.get(url_for('orders_update_page'),follow_redirects=True)
        assert response.status_code == 200
        assert response.data != ''
        
##d. delete orders - test page response, redirect, deletion of record(s)