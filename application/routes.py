from flask import Flask, redirect, request, url_for,render_template
from application import app, db
from application.models import Products,Orders,Customers #,SummaryOrder,OrdersSummary,ItemTable,OrdersTable,,CustomersTable
import sqlalchemy as sql
import pandas as pd
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html',title='home')


# create customers

@app.route('/customers/add', methods=['GET','POST'])
def add_customer():
    return ('<h1>Add New Customer</h1><br>' + render_template('customerform.html',title='add_customer')
            +('<br><br> <a href="/customers" type="button">Return to Customers home</a> </br>')
            + ('<br> <a href="/customers/update2" type="button">Update customer records</a> </br>')
            + ('<br> <a href="/" type="button">Return to home</a> </br>'))

@app.route('/customers/add/customer',methods=['GET','POST'])
def add_customers():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    if request.method=='POST':
        if len(df.loc[(df.first_name == request.form['first_name']) & (df.last_name == request.form['last_name']) & ((df.customer_dob == request.form['customer_dob'])|(df.customer_address == request.form['customer_address']))]) == 0: 
            new_first_name = request.form['first_name']
            new_last_name = request.form['last_name']
            new_customer_address = request.form['customer_address']
            new_customer_dob = request.form['customer_dob']
            new_customer = Customers(first_name=new_first_name,last_name=new_last_name,customer_address=new_customer_address,customer_dob=new_customer_dob)#,prepaid_balance=new_prepaid_balance)
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('read_customers'))
        else:
            return ("<h4><br>"+"It looks like " + str(request.form['first_name']) + " " + str(request.form['last_name'])+ " already exists in the system." + "</h4>" + '<a href="/customers/add" type="button">Try again?</a> </br>'
                    + ('<br><br> <a href="/customers/update2" type="button">Update customer records</a> </br>')+('<br> <a href="/customers" type="button">Return to Customers home</a> </br>'))


# read customers

@app.route('/customers')
def read_customers():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    df.rename(columns={'id':'Customer ID','first_name':'First Name','last_name':'Surname','customer_address':'Address','customer_dob':'Date of Birth'},inplace=True)
    html = df.to_html()

    return ('<h1>Customers</h1><br>')+html+('<br> <a href="/customers/add" type="button">Add new customer</a> </br>')+('<br> <a href="/customers/update2" type="button">Edit customer records (Update/Delete)</a> </br>')+('<br><br><br> <a href="/products">Navigate to Products</a><br><br>')+('<a href="/orders">Navigate to Orders</a>')+('<br><br> <a href="/" type="button">Return to Home</a> </br>')


# update customers

@app.route('/customers/update2')
def customer_update_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    df1 = df.copy()
    df1['Update'] = 'update'
    df1['Delete'] = 'delete'
    for n in range(len(df1)):
        df1.iloc[n,-1] = "<a href=/customers/delete/"+ str(df1.loc[n,'id']) + ">delete</a>"
        df1.iloc[n,-2] = "<a href=/customers/update/"+ str(df1.loc[n,'id']) + ">update</a>"
    df1.rename(columns={'id':'Customer ID','first_name':'First Name','last_name':'Surname','customer_address':'Address','customer_dob':'Date of Birth'},inplace=True)
    html = df1.to_html(render_links=True,escape=False)
    return ('<h1>Update Customers</h1><br>')+ html + ('<br> <a href="/customers">Back to Customers</a> </br>') + ('<br> <a href="/products">Navigate to Products</a> </br>') + ('<br> <a href="/orders">Navigate to Orders</a> </br>')

@app.route('/customers/update', methods = ['GET','POST'])
def update_customer():
    update_record = Customers.query.filter_by(id=request.form['entry']).first()
    if request.method=='POST':
        update_record = Customers.query.filter_by(id=request.form['entry']).first()
        update_record.first_name = request.form['first_name']
        update_record.last_name = request.form['last_name']
        update_record.customer_address = request.form['customer_address']
        update_record.customer_dob = request.form['customer_dob']
    db.session.commit()
        
    return redirect(url_for('read_customers'))

@app.route('/customers/update/<int:customer_record>',methods=['GET','POST'])
def customer_update1(customer_record):
    people = str(customer_record)
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    df1 = df.loc[df.id==int(customer_record),:]
    df1.rename(columns={'id':'Customer ID','first_name':'First Name','last_name':'Surname','customer_address':'Address','customer_dob':'Date of Birth'},inplace=True)
    html = df1.to_html(escape=False)
    record_no = customer_record    
    return ('<h1>Update Customers</h1><br>')+ html + "<br><br>" + render_template('customer_update.html',value=record_no) +('<br> <a href="/customers">Back to Customers</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')


# delete customers

@app.route('/customers/delete/<int:customer_>')
def delete_customers(customer_):
    if Orders.query.filter_by(fk_customer_id=customer_).count() == 0:
        customer_to_delete = Customers.query.filter_by(id=customer_).first()
        db.session.delete(customer_to_delete)
        db.session.commit()
        return redirect(url_for('read_customers'))
    else: 
        return "Oops! The customer you tried to delete has already placed an order. Please update the orders records if you need to remove this customer." +('<br> <a href="/customers">Return to Customers?</a> </br>')
    

# create products

@app.route('/products/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        page = ''
    return '<h1>Add New Product</h1><br>'+ render_template('stockform.html',title='add_item')+('<br><br> <a href="/products" type="button">Return to Products home</a> </br>')+ ('<br> <a href="/products/update2" type="button">Update product records</a> </br>')

@app.route('/products/add/item',methods=['GET','POST'])
def add_products():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    if request.method=='POST':
        if len(df.loc[(df.product_name == request.form['product_name']) & (df.product_brand == request.form['brand'])]) == 0: 
            new_product_name = request.form['product_name']
            new_product_brand = request.form['brand']
            new_product_quantity = request.form['quantity']
            new_product_itemcost = request.form['itemcost']
            new_product_price = request.form['price']
            new_product = Products(product_name=new_product_name,product_brand=new_product_brand,quantity_in_stock=new_product_quantity,cost_per_item=new_product_itemcost,price=new_product_price)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('read_products'))
        else:
            return ("<h4><br>"+"It looks like " + str(request.form['brand']) + " " + str(request.form['product_name'])+ " already exists in the system." + "</h4>" + '<a href="/products/add" type="button">Try again?</a> </br>'
                    + ('<br><br> <a href="/products/update2" type="button">Update products records</a> </br>')+('<br> <a href="/products" type="button">Return to Products home</a> </br>')+('<br> <br><a href="/" type="button">Return to Home</a> </br>'))
    

# read products

@app.route('/products')
def read_products():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    df.price = ('£'+df.price.astype('str')).str.ljust(5,'0')
    df.cost_per_item = ('£'+df.cost_per_item.astype('str')).str.ljust(5,'0')
    df.rename(columns={'id':'Product ID','product_name':'Product','product_brand':'Brand','quantity_in_stock':'Quantity in stock','cost_per_item':'Individual Cost','price':'Price'},inplace=True)
    html = df.to_html()
    return ('<h1>Products</h1><br>')+html+('<br> <a href="/products/add">Add new item to stocklist</a> </br>')+('<br> <a href="/products/update2">Edit stocklist (Update/Delete)</a> </br><br>')+('<br><br> <a href="/orders">Navigate to Orders</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>') +('<br><br> <a href="/" type="button">Return to Home</a> </br>')


# update products

@app.route('/products/update2')
def products_update_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    df1 = df.copy()
    df1['Update'] = 'update'
    df1['Delete'] = 'delete'
    for n in range(len(df1)):
        df1.iloc[n,-1] = "<a href=/products/delete/"+ str(df1.loc[n,'id']) + ">delete</a>"
        df1.iloc[n,-2] = "<a href=/products/update/"+ str(df1.loc[n,'id']) + ">update</a>"
    df1.price = ('£' + df1.price.astype('str')).str.ljust(5,'0')
    df1.cost_per_item = ('£' + df1.cost_per_item.astype('str')).str.ljust(5,'0')
    df1.rename(columns={'id':'Product ID','product_name':'Product','product_brand':'Brand','quantity_in_stock':'Quantity in stock','cost_per_item':'Individual Cost','price':'Price'},inplace=True)
    html = df1.to_html(render_links=True,escape=False)
    return ('<h1>Update Product List</h1><br>')+ html +('<br> <a href="/products">Back to Products home</a> </br>')+('<br> <br><a href="/customers">Navigate to Customers</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')+('<br> <br><a href="/" type="button">Return to Home</a> </br>')

@app.route('/products/update', methods = ['GET','POST'])
def update_product():
    if request.method=='POST':
        update_record = Products.query.filter_by(id=request.form['entry']).first()
        update_record.product_name = request.form['product_name']
        update_record.product_brand = request.form['product_brand']
        update_record.price = request.form['price']
        update_record.quantity_in_stock = request.form['quantity_in_stock']
        update_record.cost_per_item = request.form['cost_per_item']
        db.session.commit()
    return redirect(url_for('products_update_page'))

@app.route('/products/update/<int:product_record>',methods=['GET','POST'])
def product_update1(product_record):
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    df1 = df.loc[df.id==int(product_record),:]
    df1.rename(columns={'id':'Product ID','product_name':'Product','product_brand':'Brand','quantity_in_stock':'Quantity in stock','cost_per_item':'Individual Cost','price':'Price'},inplace=True)
    html = df1.to_html(escape=False)
    record_no = product_record
    return ('<h1>Update Products List</h1><br>')+html + "<br><br>" + render_template('product_update.html', value1 = record_no) + ('<br> <a href="/products">Back to Products</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')+('<br> <a href="/products" type="button">Return to Products home</a> </br>')+('<br> <br><a href="/" type="button">Return to Home</a> </br>')


# delete products

@app.route('/products/delete/<int:product_>',methods=['GET','POST'])
def delete_products(product_):
    if Orders.query.filter_by(fk_product_id=product_).count() == 0:
        product_to_delete = Products.query.filter_by(id=product_).first()
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(url_for('read_products'))
    else: return "Oops! You tried to delete a product that has already been purchased"+('<br> <br><a href="/products/update2">Try Again?</a> </br>')+('<br> <br><br><a href="/products">Return to Products</a> </br>') +('<br> <a href="/products" type="button">Return to Products home</a> </br>')+('<br> <br><a href="/" type="button">Return to Home</a> </br>')


# create orders

@app.route('/orders/add', methods = ['GET','POST'])
def add_order():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    df.price = ('£' + df.price.astype('str')).str.ljust(5,'0')
    df.rename(columns={'id':'Product ID'})
    df2 = pd.read_sql_table('customers', sql_engine,parse_dates='customer_dob')
    df['_______________________'] = ''
    df_join = pd.concat([df,df2],axis=1).fillna('.')
    date = datetime.today().strftime('%Y-%m-%d')
    df_join['Age'] = (datetime.today() - df_join.customer_dob).astype('str').str.split(' ').str[0]
    df_join.Age = (df_join.Age.astype('int')/365).astype('int')
    df_join.drop(columns=['cost_per_item','customer_dob','customer_address'],inplace=True)
    df_join.rename(columns={'id':'Customer ID','product_name':'Product','price':'Price','product_brand':'Brand','quantity_in_stock':'Quantity in stock','first_name':'First Name','last_name':'Last Name'},inplace=True)
    html = df_join.to_html(escape=False)  
    return '<h1>Add New Order</h1><br>' + render_template('orderform.html',title='add_order', value = date) + '<br><br>' + html +('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')

@app.route('/orders/add/order',methods=['GET','POST'])
def add_orders():
    if request.method=='POST':
        if int(request.form['quantity_ordered']) <= int(Products.query.filter_by(id = int(request.form['fk_product_id'])).first().quantity_in_stock):
            new_purchase_date = request.form['date']
            new_product_price = request.form['price']
            new_cash_payment = request.form['cash_payment']
            new_fk_customer_id = request.form['fk_customer_id']
            new_fk_product_id = request.form['fk_product_id']
            new_quantity_ordered = request.form['quantity_ordered']
            if round(float(request.form['cash_payment']),2) == round(float(Products.query.filter_by(id = new_fk_product_id).first().price) * (float(request.form['quantity_ordered'])),2):
                if round(float(new_product_price),2) == round(float(Products.query.filter_by(id = new_fk_product_id).first().price),2):
                    Products.query.filter_by(id = int(new_fk_product_id)).first().quantity_in_stock = int(Products.query.filter_by(id = int(new_fk_product_id)).first().quantity_in_stock) - int(new_quantity_ordered)
                    db.session.commit()
                    new_order = Orders(purchase_date=new_purchase_date,price=new_product_price,cash_payment=new_cash_payment,quantity_ordered=new_quantity_ordered,fk_customer_id=new_fk_customer_id,fk_product_id=new_fk_product_id)#,prepaid_payment=new_prepaid_payment
                    db.session.add(new_order)
                    db.session.commit()
                    return redirect(url_for('read_orders'))
                else:
                    return str(round(float(Products.query.filter_by(id = new_fk_product_id).first().price),2))+ "Oops, that wasn't the right price"+('<br> <a href="/orders/add">Try again?</a> </br>')
            else:
                return ("<h3><br>Oops, that wasn't right. The total price should be " + "£"+str(round((float(Products.query.filter_by(id = new_fk_product_id).first().price)) * float(request.form['quantity_ordered']),2)).ljust(4,'0') +"</h3>"+
                            ('<br> <a href="/orders/add">Try Again?</a> </br>') +
                            ('<br> <a href="/orders/update2">Update Orders table</a> </br>') +
                            ('<br> <br><a href="/orders">Return to Orders home</a> </br>')+
                            ('<br> <a href="/">Return to Home</a> </br>'))
        else: 
            return ("<h3><br>Sorry, there isn't enough of that product in stock</h3>" +
                        ('<br> <a href="/orders/add">Try Again?</a> </br>') +
                        ('<br> <a href="/orders/update2">Update Orders table</a> </br>') +
                        ('<br> <br><a href="/orders">Return to Orders home</a> </br>')+
                        ('<br> <a href="/">Return to Home</a> </br>'))


### read orders

@app.route('/orders')
def read_orders():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df1 = pd.read_sql_table('customers', sql_engine)
    df2 = pd.read_sql_table('products', sql_engine)
    df_join = pd.merge(left=(pd.merge(df,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['purchase_date','first_name','last_name','product_name','product_brand','price_x','quantity_ordered','id_x']]
    df_join.price_x = ('£'+df_join.price_x.astype('str')).str.ljust(5,'0')
    df_join.rename(columns={'purchase_date':'Date','first_name':'First Name','last_name':'Surname','product_name':'Product','product_brand':'Brand','price_x':'Price','quantity_ordered':'Quantity','id_x':'Order ID'},inplace=True)
    html = df_join.to_html()
    return ('<h1>Orders</h1><br>')+ html + ('<br><a href="/orders/add">Add new order</a> </br><br>')+('<a href="/orders/update2">Edit order records (Update/Delete)</a> </br>')+('<br><br><br> <a href="/products">Navigate to Products</a> </br><br>')+(' <a href="/customers">Navigate to Customers</a> </br>')+('<br> <br><a href="/">Return to Home</a> </br>')


# update order

@app.route('/orders/update2')
def orders_update_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df1 = pd.read_sql_table('customers', sql_engine)
    df2 = pd.read_sql_table('products', sql_engine)
    df_join = pd.merge(left=(pd.merge(df,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['id_x','purchase_date','first_name','last_name','product_name','product_brand','price_x','quantity_ordered']]
    df_join['Update'] = 'update'
    df_join['Delete'] = 'delete'
    for n in range(len(df_join)):
        df_join.iloc[n,-1] = "<a href=/orders/delete/"+ str(df_join.loc[n,'id_x']) + ">delete</a>"
        df_join.iloc[n,-2] = "<a href=/orders/update/"+ str(df_join.loc[n,'id_x']) + ">update</a>"
    df_join.price_x = ('£' + df_join.price_x.astype('str')).str.ljust(5,'0')
    df_join.rename(columns={'purchase_date':'Date','first_name':'First Name','last_name':'Surname','product_name':'Product','product_brand':'Brand','price_x':'Price','quantity_ordered':'Quantity','id_x':'Order ID'},inplace=True)
    html = df_join.to_html(render_links=True,escape=False,classes='table table-striped')
    return ('<h1>Update Orders</h1><br>')+html+('<br> <a href="/orders">Back to Orders</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+(' <a href="/customers">Navigate to Customers</a> </br>')

@app.route('/orders/update', methods = ['GET','POST'])
def update_order():
    if request.method=='POST':
        update_record = Orders.query.filter_by(id=request.form['entry']).first()
        update_quantity_ordered = request.form['quantity_ordered']
        
        if update_record.fk_product_id != request.form['fk_product_id']:
            if (float(request.form['price']) == float(Products.query.filter_by(id=int(request.form['fk_product_id'])).first().price)) & (float(request.form['cash_payment']) == float(request.form['price']) * int(update_quantity_ordered)):
                update_record.price = request.form['price']
                
                update_record.purchase_date = request.form['purchase_date']
                update_record.price = request.form['price']
                update_record.cash_payment = request.form['cash_payment']
                update_record.fk_customer_id = request.form['fk_customer_id']

                Products.query.filter_by(id=update_record.fk_product_id).first().quantity_in_stock = int(Products.query.filter_by(id = int(update_record.fk_product_id)).first().quantity_in_stock) + (int(update_record.quantity_ordered))
                db.session.commit()
                update_record.fk_product_id = request.form['fk_product_id']
                update_record.quantity_ordered = request.form['quantity_ordered']
                Products.query.filter_by(id=update_record.fk_product_id).first().quantity_in_stock = int(Products.query.filter_by(id = int(update_record.fk_product_id)).first().quantity_in_stock) - (int(update_record.quantity_ordered)-(int(update_record.quantity_ordered)-int(update_quantity_ordered)))
                db.session.commit()    
                return redirect(url_for('read_orders'))
            else:
                return "Something wasn't right there. Your latest changes have not been logged in the system"

        elif update_record.fk_product_id == request.form['fk_product_id']:
            update_record.purchase_date = request.form['purchase_date']
            update_record.price = request.form['price']
            update_record.cash_payment = request.form['cash_payment']
            update_record.fk_customer_id = request.form['fk_customer_id']
            
            db.session.commit()
            update_record.fk_product_id = request.form['fk_product_id']
            update_record.quantity_ordered = request.form['quantity_ordered']
            return redirect(url_for('read_orders'))


@app.route('/orders/update/<int:order_record>',methods=['GET','POST'])
def order_update1(order_record):
    if request.method == 'POST':
        connect_string = ""
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df_row = df.loc[df.id==int(order_record),:]
    df1 = pd.read_sql_table('customers', sql_engine)
    df2 = pd.read_sql_table('products', sql_engine)
    df_join = pd.merge(left=(pd.merge(df_row,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['id_x','purchase_date','price_x','quantity_ordered','cash_payment','price_x','fk_customer_id','fk_product_id','first_name','last_name','product_name','product_brand']]
    df_join.rename(columns={'fk_product_id':'Product ID','fk_customer_id':'Customer ID','purchase_date':'Date','first_name':'First Name','last_name':'Surname','product_name':'Product','product_brand':'Brand','price_x':'Price','quantity_ordered':'Quantity','id_x':'Order ID'},inplace=True)
    order_no = order_record
    html = df_join.to_html(escape=False,classes='table table-striped')
    return ('<h1>Update Orders</h1><br>')+html + "<br><br>" + render_template('orders_update.html', value1=order_no)


# delete order

@app.route('/orders/delete/<int:order_>', methods = ['GET','POST'])
def delete_orders(order_):
    if request.method == 'POST':
        page=''
    order_to_delete = Orders.query.filter_by(id=order_).first()
    order_fk_id = order_to_delete.fk_product_id
    Products.query.filter_by(id = int(order_to_delete.fk_product_id)).first().quantity_in_stock = int(Products.query.filter_by(id = int(order_to_delete.fk_product_id)).first().quantity_in_stock) + int(order_to_delete.quantity_ordered)  
    db.session.delete(order_to_delete)
    db.session.commit()
    return redirect(url_for('read_orders'))




