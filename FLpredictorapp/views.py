#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, render_template, url_for, flash, session
import pdb

app = Flask(__name__)

app.config.from_object('config')
from .utils import load_airports, predict

@app.route('/', methods= ['GET','POST'])
@app.route('/index', methods= ['GET','POST'])
def index():
    airports = load_airports()
    if request.method == 'POST':
        # replace this with an insert into whatever database you're using
        return redirect(url_for('test'))
        #return flash('Yor request is sent.')
    return render_template('form.html', title = "Airline Info",
                            airports = airports)

@app.route('/test', methods= ['GET','POST'])

def test():
    origin_iata = request.form["origin"]
    dest_iata = request.form["dest"]
    time = request.form["dep_time"]
    date = request.form["dep_day"]
    departed = request.form["departed"]
    carrier = request.form["carrier"]

    # predict
    y_pred, rmse_score_test = predict(origin_iata, dest_iata, date, time,
                                     departed, carrier)
    y_pred = int(y_pred[0])
    rmse_score_test = int(rmse_score_test)

    return render_template('test.html',title = "Airline Info",
                            origin_iata=origin_iata, dest_iata=dest_iata,
                            time=time, date=date,departed=departed,
                            carrier=carrier, y_pred=y_pred,
                            rmse_score_test=rmse_score_test)
