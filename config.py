import os

SECRET_KEY = '#d#JCqTTW\nilK\\7m\x0bp#\tj~#H'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Database initialization
if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    DATABASE_URI = os.path.join(basedir, 'FLpredictorapp/static/db/')

else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DATABASE_URI = '/FLpredictorapp/static/db/'
