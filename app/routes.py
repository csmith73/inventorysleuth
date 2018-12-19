from app import app
from flask import render_template


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('user_dashboard.html')

@app.route("/login")
def login():
    return render_template('login.html')














