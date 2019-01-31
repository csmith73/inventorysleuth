from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class sellerinventory(db.Model):
    asin = db.Column(db.String())
    sellername = db.Column(db.String())
    listingid = db.Column(db.String(), primary_key=True)
    date = db.Column(db.Date())
    inventory = db.Column(db.Integer)

class trackedproducts(db.Model):
    asin = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    link = db.Column(db.String())
    picture = db.Column(db.String())
    bsr_rank = db.Column(db.Integer)
    bsr_category = db.Column(db.String())

class usertrackedproducts(db.Model):
    asin = db.Column(db.String())
    username = db.Column(db.String())
    id = db.Column(db.String(), primary_key=True)

class productinventory(db.Model):
    asin = db.Column(db.String())
    seller = db.Column(db.String())
    date = db.Column(db.String())
    inventory =db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)




