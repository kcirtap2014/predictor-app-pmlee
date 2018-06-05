from flask_sqlalchemy import SQLAlchemy
import config as CONFIG
import pandas as pd
import logging as lg
from sklearn.externals import joblib
import pdb

from .views import app
# Create database connection object

db = SQLAlchemy(app)

class Airports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(5), nullable=False)
    iata = db.Column(db.String(3), nullable=False)

    def __init__(self, name, city, state, iata,):
        self.name = name
        self.city = city
        self.state = state
        self.iata = iata

def load_data(filename):
    data = pd.read_csv(CONFIG.DATABASE_URI+filename)
    return data

def load_joblib(filename):
    data = joblib.load(CONFIG.DATABASE_URI+filename)
    return data

def init_db():
    db.drop_all()
    db.create_all()
    data = load_data("apsearch_US.csv")
    data = data.sort_values(by="STATE").reset_index().drop(columns="index")
    for index in range(len(data)):
        db.session.add(Airports(data.loc[index, "NAME"],data.loc[index, "CITY"], data.loc[index,"STATE"],data.loc[index,"IATA"]))
    db.session.commit()
    lg.warning('Database initialized!')
