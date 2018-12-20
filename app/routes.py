from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, trackedproducts, sellerinventory, usertrackedproducts
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
        row = trackedproducts.query.filter(trackedproducts.asin == item).all()[0]
        print(row.asin)
        d = collections.OrderedDict()
        d['asin'] = row.asin
        d['name'] = row.name
        d['link'] = row.link
        d['picture'] = row.picture
        d['bsr_rank'] = row.bsr_rank
        d['bsr_category'] = row.bsr_category
        objects_list.append(d)

    dump = {"data": objects_list}
    return json.dumps(dump)











