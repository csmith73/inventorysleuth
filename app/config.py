import os
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(os.path.dirname(__file__), 'inventorysleuth.db')
print(db_path)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False