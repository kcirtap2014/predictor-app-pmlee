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
    origin_name = db.Column(db.String(50), nullable=False)
    dest_name = db.Column(db.String(50), nullable=False)
    origin_city = db.Column(db.String(10), nullable=False)
    dest_origin_city = db.Column(db.String(10), nullable=False)
    origin_state = db.Column(db.String(5), nullable=False)
    dest_state = db.Column(db.String(5), nullable=False)
    origin_iata = db.Column(db.String(3), nullable=False)
    dest_iata = db.Column(db.String(3), nullable=False)
    carrier = db.Column(db.String(2), nullable=False)

    def __init__(self, origin_name, origin_city, origin_state, origin_iata,
    dest_name, dest_city, dest_state, dest_iata, carrier):
        self.origin_name = origin_name
        self.origin_city = origin_city
        self.origin_state = origin_state
        self.origin_iata = origin_iata
        self.dest_name = dest_name
        self.dest_city = dest_city
        self.dest_state = dest_state
        self.dest_iata = dest_iata
        self.carrier = carrier

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
    data = data.sort_values(by="ORIGIN_STATE").reset_index().drop(columns="index")

    for index in range(len(data)):
        db.session.add(Airports(data.loc[index, "ORIGIN_NAME"],
        data.loc[index, "ORIGIN_CITY"], data.loc[index,"ORIGIN_STATE"], data.loc[index,"ORIGIN_IATA"], data.loc[index, "DEST_NAME"],
        data.loc[index, "DEST_CITY"], data.loc[index,"DEST_STATE"],
        data.loc[index,"DEST_IATA"]))
    db.session.commit()
    lg.warning('Database initialized!')
