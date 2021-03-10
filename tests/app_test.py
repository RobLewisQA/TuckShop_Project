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

#2. Customers
##a. add customers - test page response, return template, redirect, post

#def test_home_redir():
#    response = app.test_client().get('/home')
#    assert response.status_code == 200
#    assert response.data != ''

##b. read customers - test page response, links
    def test_read_customers(self):
        response = self.client.get(url_for('read_customers'))
        assert response.status_code == 200
        assert response.data != ''
##c.update customers - test update page response, table, links
##c. update customers2 - test form response, table view, post

##d. delete customers - test page response, redirect, deletion of record(s)

#3. Products
##a. add products - test page response, return template, redirect, post
    def test_read_products(self):
        response = self.client.get(url_for('read_products'))
        assert response.status_code == 200
        assert response.data != ''
##b. read products - test page response, links
##c.update products - test update page response, table, links
##c. update products2 - test form response, table view, post
##d. delete products - test page response, redirect, deletion of record(s)
#4. Orders
##a. add orders - test page response, return template, redirect, post
##b. read orders - test page response, links
    def test_read_orders(self):
        response = self.client.get(url_for('read_orders'))
        assert response.status_code == 200
        assert response.data != ''
##c.update orders - test update page response, table, links
##c. update orders - test form response, table view, post
##d. delete orders - test page response, redirect, deletion of record(s)