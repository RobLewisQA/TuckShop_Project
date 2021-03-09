from application import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DecimalField, widgets, SelectMultipleField
from application.models import Customers
#################################################
'''
class BasicForm_orders(FlaskForm):
    purchase_date = DateField('Purchase Date')
    price = DecimalField('Price')
    cash_payment = DecimalField('Price')
    prepaid_payment = DecimalField('Price')
    submit = SubmitField('Add Order')
'''
##################################################
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
##################################################
class BasicForm_customers(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    customer_address = StringField('Address')
    customer_dob = DateField('Date of Birth')
    prepaid_balance = DecimalField('Prepaid Balance')
    submit = SubmitField('Add Customer')
##################################################
'''
class MultiCheckboxField_customers(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SimpleForm_customers(FlaskForm):
    #string_of_files = Customers.query.all()
    list_of_files = Customers.query.all()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField_customers('Label', choices=files)
'''
##################################################

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')