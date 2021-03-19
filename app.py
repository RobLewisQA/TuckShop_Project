from application import app
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField, DateField, DecimalField, widgets, SelectMultipleField
#from application.models import Customers

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')