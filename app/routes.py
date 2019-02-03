from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, trackedproducts, sellerinventory, usertrackedproducts, productinventory
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
import collections
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('user_dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/product_table_populate', methods=['GET', 'POST'])
def product_table_populate():
    user = str(request.json)
    print(user)
    asin_list = []
    for row in usertrackedproducts.query.filter(usertrackedproducts.username == user).all():
        asin = row.asin
        asin_list.append(asin)
    print(asin_list)



    objects_list = []
    for item in asin_list:
        print(item)
        row = trackedproducts.query.filter(trackedproducts.asin == item).first()
        print(row.asin)
        d = collections.OrderedDict()
        d['asin'] = '<a href=productinventory/' + row.asin + '>' + row.asin + '</a>'
        d['name'] = row.name
        d['link'] = '<a href=' + row.link + ' target="_blank">' + 'Product Link' + '</a>'
        d['picture'] = row.picture
        d['bsr_rank'] = row.bsr_rank
        d['bsr_category'] = row.bsr_category
        objects_list.append(d)

    print(objects_list)
    dump = {"data": objects_list}
    table_data = json.dumps(dump)
    print(table_data)
    return table_data


@app.route('/productinventory/<asin>', methods=['GET', 'POST'])
def productinventory_page(asin):
    print(asin)
    cur_asin = str(asin)
    title_data = trackedproducts.query.filter(trackedproducts.asin == cur_asin).all()[0]
    print(title_data)
    cur_title = title_data.name
    print(cur_title)
    return render_template('productinventory_page.html',cur_asin=cur_asin, cur_title=cur_title)

@app.route('/get_inventory', methods=['GET', 'POST'])
def get_inventory():
    asin = request.get_json()
    print(asin)
    print(".............................")
    data = productinventory.query.filter(productinventory.asin == asin).all()
    print(data)
    dates = [row.date for row in data]
    dates = list(set(dates))
    print(dates)

    sellers = [row.seller for row in data]
    sellers = list(set(sellers))
    print(sellers)

    # SELECT DISTINCT date FROM productinventory WHERE asin='B000YD02MK'

    t_data = []
    for seller in sellers:
        single_data = productinventory.query.filter(productinventory.seller == seller)
        print(single_data)
        date_inv_dict = {'seller':seller}
        for s_row in single_data:
            s_date = s_row.date
            s_inventory = s_row.inventory
            date_inv_dict[s_date] = s_inventory
            print(date_inv_dict)
        t_data.append(date_inv_dict)
        print(t_data)


    print(t_data)

    columns = list(t_data[0].keys())
    print(columns)
    col_list = []
    for col in columns:
        #col_dict = {'data':col}
        #col_list.append(col_dict)
        col_dict = {'data':col}
        col_dict['title'] = col
        col_list.append(col_dict)
    print(col_list)
    dump = {"columns":col_list, "data": t_data}
    print(dump)
    table_data = json.dumps(dump)
    print(table_data)
    return table_data







