from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@34.89.69.248/Tuckshop" # Set the connection string to connect to the database
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from application import routes