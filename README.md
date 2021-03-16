# Tuckshop 
## Application Overview
### Tuckshop is a web application for use by a tuckshop vendor for recording product sales. It is designed for a youth camp, where a customer list, as well as the stock list, is known. All tables accomodate the addition, updating and deletion of records - it is assumed that the tuckshop vendor will be the only user, so there is no restricted functionality.

### The tables are configured so that new orders added will remove the quantity ordered from the stock-list and deleted orders will restore the quantity ordered. Updating an order with a different product will act like the deletion of the previous order and the creation of a new order, and this will be reflected in the orders and products tables.                  

## Technologies
### Cloud Server Host:
#### Google CLoud PLatform
### Database host format:
#### MySQL
### Frontend script:
#### html
### Integration software:
#### python3, pandas, SQLAlchemy
### Testing software:
#### flask-testing
#### pytest
### Deployment software:
#### Flask
#### Jenkins
#### Gunicorn

# Database Relationship Flowchart

# What does the user need to do to get it working

# References:
## Pandas integreation with SQLAlchemy and HTML - Eric Brown, 2018 accessed at https://pythondata.com/quick-tip-sqlalchemy-for-mysql-and-pandas/
## HTML form creation - https://www.w3schools.com/html/html_forms.asp
