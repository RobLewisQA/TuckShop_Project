from flask import Flask, redirect, request, url_for,render_template
from application import app, db
from application.models import Products,ItemTable,Orders,OrdersTable,Customers,CustomersTable#,SummaryOrder,OrdersSummary
#from app import BasicForm_customers#, SimpleForm_customers
import sqlalchemy as sql
import pandas as pd

@app.route('/')
def home():
    return render_template('home.html',title='home')
## create customers
@app.route('/customers/add', methods=['GET','POST'])
def add_customer():
    if request.method == 'POST':
        page = ''
    return render_template('customerform.html',title='add_customer')

@app.route('/customers/add/customer',methods=['GET','POST'])
def add_customers():
    if request.method=='POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_customer_address = request.form['customer_address']
        new_customer_dob = request.form['customer_dob']
        new_prepaid_balance = request.form['prepaid_balance']
        new_customer = Customers(first_name=new_first_name,last_name=new_last_name,customer_address=new_customer_address,customer_dob=new_customer_dob,prepaid_balance=new_prepaid_balance)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('read_customers'))

##### test add_customer ####
#@app.route('/customers/add/customer_test',methods=['GET','POST'])
#def add_customer_test():
#        error = ""
#        form = BasicForm_customers()##
#
#        if request.method == 'POST':
#            first_name = form.first_name#.data
#            last_name = form.last_name#.data
#            customer_address = form.customer_address.data
#            customer_dob = form.customer_dob.data
#            prepaid_balance = form.prepaid_balance.data#
#
#            if len(first_name) == 0 or len(last_name) == 0:
#                error = "That didn't work"
#            else:
#                return 'thank_you'

        return render_template('customerform_wtf.html', form=form, message=error)

###################

## read customers
@app.route('/customers')
def read_customers():
    #people = Customers.query.all()
    #table = CustomersTable(people)

    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    html = df.to_html()

    return ('<h1>Customers</h1><br>')+html+('<br> <a href="/customers/add" type="button">Add new customer</a> </br>')+('<br> <a href="/customers/delete" type="button">Delete customer</a> </br>')+('<br> <a href="/customers/update2" type="button">Update customer records</a> </br>')+('<br><br> <a href="/products">Navigate to Products</a><br>')+('<a href="/orders">Navigate to Orders</a>')
    #('<h1>Customers</h1><br>')+table.__html__()+('<br> <a href="/customers/add" type="button">Add new customer</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')


## update customers
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
    html = df1.to_html(render_links=True,escape=False)
    return ('<h1>Update Customers</h1><br>')+ html + ('<br> <a href="/customers">Back to Customers</a> </br>') + ('<br> <a href="/products">Navigate to Products</a> </br>') + ('<br> <a href="/orders">Navigate to Orders</a> </br>')
### customer select_test ################################################

@app.route('/customers/update', methods = ['GET','POST'])
def update_customer():
    update_record = Customers.query.filter_by(id=request.form['entry']).first()
    if request.method=='POST':
        update_record = Customers.query.filter_by(id=request.form['entry']).first()
        update_record.first_name = request.form['first_name']
        update_record.last_name = request.form['last_name']
        update_record.customer_address = request.form['customer_address']
        update_record.customer_dob = request.form['customer_dob']
        update_record.prepaid_balance = request.form['prepaid_balance']
    db.session.commit()
        
    return redirect(url_for('read_customers'))#render_template('customer_update.html',title='update_customer')

@app.route('/customers/update/<int:customer_record>',methods=['GET','POST'])
def customer_update1(customer_record):
    people = str(customer_record)
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    df1 = df.loc[df.id==int(customer_record),:]
    html = df1.to_html(escape=False)
    #customer_update_code = pd.read_html('customer_update.html')
    
    return ('<h1>Update Customers</h1><br>')+ html + "<br><br>" + render_template('customer_update.html') +('<br> <a href="/customers">Back to Customers</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')



    #connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    #sql_engine = sql.create_engine(connect_string)

    #df = pd.read_sql_table('customers', sql_engine)

    #df1 = df.drop_duplicates(['first_name','last_name','customer_dob'])
    #df1['Select'] = 'select'
    #for n in range(len(df1)):
    #    df1.iloc[n,-1] = "<a href=/customers/delete/"+ str(df1.loc[n,'id']) + ">delete</a>"

    #html = df1.to_html(render_links=True,escape=False)



    #my_conn = create_engine("mysql+pymysql://root:root@34.89.69.248/Tuckshop")
    #my_data = pd.read_sql("SELECT * FROM Customers",my_conn)
    #df = pd.DataFrame(my_data)
    
    #df = pd.read_sql(Customers.query.all(), con = "mysql+pymysql://root:root@34.89.69.248/Tuckshop")
    #df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'],'physics': [68, 74, 77, 78],'chemistry': [84, 56, 73, 69],'algebra': [78, 88, 82, 87]})
    
        ##html = df1.to_html()

    #write html to file
    #text_file = open("index1.html", "w")
    #text_file.write(html)
    #text_file.close()
    #render_template('index1.html')
    
    #str_ = []
    #people = Customers.query.all()
    #table1 = CustomersTable(people)
    ##if request.method == 'POST':
    #    return print(str(people))
    #return str(people[2])


        #print(request.form.getlist('my_checkbox'))
    #    return render_template('customer_table_temp.html')
    #return table1.astype('str')
    #for n in range(len(table1.__html__().split('<tr'))):
    #    str_.append(str(table1.__html__().split('<tr')[2]) + '/')
    #for s in str_:
    #    return s



'''
@app.route('/customers/update',methods=['post','get'])
def update_customers():
    form = SimpleForm_customers()
    if form.validate_on_submit():
        print(form.example.data)
        return form.example.data
    else:
        print("Validation Failed")
        print(form.errors)
    return render_template('customerform_wtf.html',form=form)
'''
##########################################################################

## delete customers
@app.route('/customers/delete/<int:customer_>', methods = ['GET','POST'])
def delete_customers(customer_):
    if request.method=='POST':
        if Orders.query.filter_by(fk_customer_id=customer_).count() == 0:
            customer_to_delete = Customers.query.filter_by(id=customer_).first()
            db.session.delete(customer_to_delete)
            db.session.commit()
            return redirect(url_for('read_customers'))
        else: 
            return "Oops! You tried to delete a product that has already been purchased" +('<br> <a href="/customers">Return to Customers?</a> </br>')

@app.route('/customers/delete', methods=['GET','POST'])
def customer_delete_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('customers', sql_engine)
    df1 = df.copy()
    df1['Select'] = 'select'
    for n in range(len(df1)):
        df1.iloc[n,-1] = "<a href=/customers/delete/"+ str(df1.loc[n,'id']) + ">delete</a>"
    html = df1.to_html(render_links=True,escape=False)
    return html
## create products
@app.route('/products/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        page = ''
    return render_template('stockform.html',title='add_item')

@app.route('/products/add/item',methods=['GET','POST'])
#('/products/add/?name=<name_>&brand=<brand_>&quantity=<quantity_>&cost=<itemcost>&price=<price_>')
#'/products/add/<name>-<brand>-<quantity>-<itemcost>-<price_>'
def add_products():
    if request.method=='POST':
        new_product_name = request.form['name']
        new_product_brand = request.form['brand']
        new_product_quantity = request.form['quantity']
        new_product_itemcost = request.form['itemcost']
        new_product_price = request.form['price']
        new_product = Products(product_name=new_product_name.replace('_',' '),product_brand=new_product_brand.replace('_',' '),quantity_in_stock=new_product_quantity,cost_per_item=new_product_itemcost,price=new_product_price)
        db.session.add(new_product)
        db.session.commit()
    return redirect(url_for('read_products'))

## read products
@app.route('/products')
def read_products():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    
    #df.loc[df.cost_per_item.str.len() <5]
    df.price = ('£'+df.price.astype('str')).str.ljust(5,'0')
    df.cost_per_item = ('£'+df.cost_per_item.astype('str')).str.ljust(5,'0')
    html = df.to_html()
    #items = Products.query.all()
    #table = ItemTable(items)
    return ('<h1>Products</h1><br>')+html+('<br> <a href="/products/add">Add new item to stocklist</a> </br>')+('<br> <a href="/products/update2">Edit stocklist</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')

## update products
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
    html = df1.to_html(render_links=True,escape=False)
    return ('<h1>Update Product List</h1><br>')+ html +('<br> <a href="/products">Back to Products</a> </br>')+('<br> <a href="/Customers">Navigate to Customers</a> </br>')+('<br> <a href="/Orders">Navigate to Orders</a> </br>')

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
        
    return redirect(url_for('read_products'))#render_template('customer_update.html',title='update_customer')

@app.route('/products/update/<int:product_record>',methods=['GET','POST'])
def product_update1(product_record):
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    df1 = df.loc[df.id==int(product_record),:]
    html = df1.to_html(escape=False)
    #customer_update_code = pd.read_html('customer_update.html')
    return ('<h1>Update Products List</h1><br>')+html + "<br><br>" + render_template('product_update.html') + ('<br> <a href="/products">Back to Products</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')+('<br> <a href="/orders">Navigate to Orders</a> </br>')

## delete products
@app.route('/products/delete/<int:product_>',methods=['GET','POST'])
def delete_products(product_):
    if Orders.query.filter_by(fk_product_id=product_).count() == 0:
        product_to_delete = Products.query.filter_by(id=product_).first()
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(url_for('read_products'))
    else: return "Oops! You tried to delete a product that has already been purchased" +('<br> <a href="/products">Return to Products?</a> </br>')

@app.route('/products/delete')
def product_delete_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('products', sql_engine)
    df1 = df.copy()
    df1['Select'] = 'select'
    for n in range(len(df1)):
        df1.iloc[n,-1] = "<a href=/products/delete/"+ str(df1.loc[n,'id']) + ">delete</a>"
    html = df1.to_html(render_links=True,escape=False)
    return html 
'''
#def read():
#    all_products = Products.query.all()
#    products_string = ""
#    for product in all_products:
#        products_string += "<br>"+ product.product_name 
#    return products_string
'''
## create orders

@app.route('/orders/add', methods = ['GET','POST'])
def add_order():
    html = ""
    if request.method == 'POST':
        connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
        sql_engine = sql.create_engine(connect_string)
        df = pd.read_sql_table('products', sql_engine)
        #df1 = df.loc[df.id==int(customer_record),:]
        html = df.to_html(escape=False)
    return render_template('orderform.html',title='add_order') + '<br><br>' + html +('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')
#return render_template('orderform.html',title='add_order') + '<br><br>' + html +('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')

#@app.route('/orders/add/order')
#def add_orders(date,price,cash_payment,prepaid_payment,fk_customer_id,fk_product_id):
#    new_product = Products(product_name=name,product_brand=brand,quantity_in_stock=quantity,cost_per_item=itemcost)
#    db.session.add(new_product)
#    db.session.commit()
#    return "Added new product to database"

@app.route('/orders/add/order',methods=['GET','POST'])
def add_orders():
    if request.method=='POST':
        new_purchase_date = request.form['date']
        new_product_price = request.form['price']
        new_cash_payment = request.form['cash_payment']
        new_prepaid_payment = request.form['prepaid_payment']
        new_fk_customer_id = request.form['fk_customer_id']
        new_fk_product_id = request.form['fk_product_id']
        if float(new_product_price) == float(Products.query.filter_by(id = new_fk_product_id).first().price):
            Products.query.filter_by(id = int(new_fk_product_id)).first().quantity_in_stock = int(Products.query.filter_by(id = int(new_fk_product_id)).first().quantity_in_stock) - 1
            db.session.commit()
            new_order = Orders(purchase_date=new_purchase_date,price=new_product_price,cash_payment=new_cash_payment,prepaid_payment=new_prepaid_payment,fk_customer_id=new_fk_customer_id,fk_product_id=new_fk_product_id)
            db.session.add(new_order)
            db.session.commit()
            return redirect(url_for('read_orders')) #f'{int(Products.query.filter_by(id = new_fk_product_id).first()).quantity_in_stock}'
        else:
            return str(float(Products.query.filter_by(id = new_fk_product_id).first().price))+ "Oops, that didn't work"+('<br> <a href="/orders/add">Try again?</a> </br>')
        #str(Products.query.filter_by(id = new_fk_product_id).first().quantity_in_stock) + str(int(Products.query.filter_by(id = new_fk_product_id).first().quantity_in_stock) - 1) + "   oops, that didn't work"+('<br> <a href="/orders/add">Try again?</a> </br>')
        #redirect(url_for('read_orders'))

##### test add ####
'''
@app.route('/orders/add/order_test',methods=['GET','POST'])
def add_order_test():
        error = ""
        form = BasicForm_orders()

        if request.method == 'POST':
            purchase_date = form.first_name.data
            last_name = form.last_name.data

        #if len(purchase_date) == 0 or len(last_name) == 0:
        #    error = "That didn't work"
        #else:
        #    return 'thank_you'

        return render_template('home.html', form=form, message=error)
'''
###################
### read orders
@app.route('/orders')
def read_orders():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df1 = pd.read_sql_table('customers', sql_engine)
    df2 = pd.read_sql_table('products', sql_engine)
    df_join = pd.merge(left=(pd.merge(df,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['purchase_date','first_name','last_name','product_name','product_brand','price_x','id_x']]
    df_join.price_x = ('£'+df_join.price_x.astype('str')).str.ljust(5,'0')
    html = df_join.to_html()
    return ('<h1>Orders</h1><br>')+ html + ('<br><a href="/orders/add">Add new order</a> </br>')+('<a href="/orders/update2">Edit an order</a> </br>')+('<br> <a href="/orders/summary">Sales summary</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+(' <a href="/customers">Navigate to Customers</a> </br>')


@app.route('/orders/summary')
def read_order_summary():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df1 = pd.read_sql_table('customers', sql_engine)
    df2 = pd.read_sql_table('products', sql_engine)
    df_join = pd.merge(left=(pd.merge(df,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['purchase_date','first_name','last_name','product_name','product_brand','price_x','id_x']]
    df_groups = df_join.groupby(['product_brand']).purchase_date.count().to_frame()
    html = df_groups.to_html()
    return ('<h1>Orders</h1><br>')+ html + ('<br> <a href="/orders">Orders Home Page</a> </br>')+('<br> <a href="/orders/add">Add new order</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+('<br> <a href="/customers">Navigate to Customers</a> </br>')

### update order

@app.route('/orders/update2')
def orders_update_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df1 = pd.read_sql_table('customers', sql_engine)
    df2 = pd.read_sql_table('products', sql_engine)
    df_join = pd.merge(left=(pd.merge(df,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['id_x','purchase_date','first_name','last_name','product_name','product_brand','price_x']]
    df_join['Update'] = 'update'
    df_join['Delete'] = 'delete'
    for n in range(len(df_join)):
        df_join.iloc[n,-1] = "<a href=/orders/delete/"+ str(df_join.loc[n,'id_x']) + ">delete</a>"
        df_join.iloc[n,-2] = "<a href=/orders/update/"+ str(df_join.loc[n,'id_x']) + ">update</a>"
    html = df_join.to_html(render_links=True,escape=False)
    return ('<h1>Update Orders</h1><br>')+html+('<br> <a href="/orders">Back to Orders</a> </br>')+('<br> <a href="/products">Navigate to Products</a> </br>')+(' <a href="/customers">Navigate to Customers</a> </br>')

@app.route('/orders/update', methods = ['GET','POST'])
def update_order():
    if request.method=='POST':
        update_record = Orders.query.filter_by(id=request.form['entry']).first()
        update_record.purchase_date = request.form['purchase_date']
        update_record.price = request.form['price']
        update_record.cash_payment = request.form['cash_payment']
        update_record.prepaid_payment = request.form['prepaid_payment']
        update_record.fk_customer_id = request.form['fk_customer_id']
        if update_record.fk_product_id != request.form['fk_product_id']:
            Products.query.filter_by(id=update_record.fk_product_id).first().quantity_in_stock = int(Products.query.filter_by(id = int(update_record.fk_product_id)).first().quantity_in_stock) + 1  
            update_record.fk_product_id = request.form['fk_product_id']
            db.session.commit()
            Products.query.filter_by(id=update_record.fk_product_id).first().quantity_in_stock = int(Products.query.filter_by(id = int(update_record.fk_product_id)).first().quantity_in_stock) - 1  
        else:
            update_record.fk_product_id = request.form['fk_product_id']
        db.session.commit()
    return redirect(url_for('read_orders'))#render_template('customer_update.html',title='update_customer')

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
    df_join = pd.merge(left=(pd.merge(df_row,df1,how='left',left_on='fk_customer_id',right_on='id')),right=df2,how='left',left_on='fk_product_id',right_on='id')[['id_x','purchase_date','price_x','cash_payment','prepaid_payment','price_x','fk_customer_id','fk_product_id','first_name','last_name','product_name','product_brand']]
    
    html = df_join.to_html(escape=False)
    #customer_update_code = pd.read_html('customer_update.html')
    return ('<h1>Update Orders</h1><br>')+html + "<br><br>" + render_template('orders_update.html')

### delete order
@app.route('/orders/delete/<int:order_>', methods = ['GET','POST'])
def delete_orders(order_):
    if request.method == 'POST':
        #order_to_delete = Orders.query.filter_by()
        order_to_delete = Orders.query.filter_by(id=order_).first()
        #order_to_delete.quantity_in_stock = Products.query.filter_by(Orders.fk_product_id = order_to_delete.)
        order_fk_id = order_to_delete.fk_product_id
        Products.query.filter_by(id = int(order_to_delete.fk_product_id)).first().quantity_in_stock = int(Products.query.filter_by(id = int(order_to_delete.fk_product_id)).first().quantity_in_stock) + 1  
        db.session.delete(order_to_delete)
        db.session.commit()
    return redirect(url_for('read_orders'))

@app.route('/orders/delete')
def order_delete_page():
    connect_string ="mysql+pymysql://root:root@34.89.69.248/Tuckshop"
    sql_engine = sql.create_engine(connect_string)
    df = pd.read_sql_table('orders', sql_engine)
    df1 = df.copy()
    df1['Select'] = 'select'
    for n in range(len(df1)):
        df1.iloc[n,-1] = "<a href=/orders/delete/"+ str(df1.loc[n,'id']) + ">delete</a>"
    html = df1.to_html(render_links=True,escape=False)
    return html
#@app.route('/products/delete/<int:order>')
#def delete_orders1(order_):
#    Products.query.filter_by(id = int(new_fk_product_id)).first().quantity_in_stock = int(Products.query.filter_by(id = int(new_fk_product_id)).first().quantity_in_stock) - 1
#    db.session.commit()
#    new_order = Orders(purchase_date=new_purchase_date,price=new_product_price,cash_payment=new_cash_payment,prepaid_payment=new_prepaid_payment,fk_customer_id=new_fk_customer_id,fk_product_id=new_fk_product_id)
##   db.session.add(new_order)
#    db.session.commit()

    #if Orders.query.filter_by(fk_product_id=product_).count() == 0:
    #    product_to_delete = Products.query.filter_by(id=product_).first()
    #    db.session.delete(product_to_delete)
    #    db.session.commit()
    #    return redirect(url_for('read_products'))
   # else: return "Oops! You tried to delete a product that has already been purchased" +('<br> <a href="/products">Return to Products?</a> </br>')

#@app.route('/orders/auto_aupdate/')
#def autoupdate_orders(order_):
#    autoupdate = Products.query.filter_by(id=order_).first()
#    autoupdate.quantity_in_stock = autoupdate.quantity_in_stock - 1
#    db.session.commit()
#    return redirect(url_for('read_orders'))
#############################################################################################



'''
@app.route('/update/<name>')
def products_update(name):
    first_product = Products.query.first()
    first_product.product_name = name
    db.session.commit()
    return first_product.product_name

## orders CRUD

create route to orders-home (redirect to orders summary)
'''







###
#@app.route('/products')
#def read_products():
#    items = Products.query.all(order_by = product_brand)

    #all_products = Products.query.all()
    #products_string = ""
    #for product in all_products:
    #    products_string += "<br>"+ product.product_name 
    #return products_string
#    table = ItemTable(items)
#    return table.__html__()
'''
@app.route('/')

def hello_internet():
    return "Hello internet"

@app.route('/users/<name>/<int:id>')
def users(name,id):
    return f"Hello, {name}, your ID is {id}"

'''
'''
@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return 'This is a POST request'
    else: 
        return 'This is a GET request'


@app.route('/home')
def home():
    return render_template('home.html',title="Home")

@app.route('/account')
def account():
    if user_logged_in() == True:
        return 'Your account balance is £n'
    else:
        return redirect(url_for('home'))

def user_logged_in():
    return False

@app.route('/users/<name>/<int:id>')
def users(name,id):
    return f"Hello, {name}, your ID is {id}"
'''