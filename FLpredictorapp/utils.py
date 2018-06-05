import pandas as pd
import logging as lg
import numpy as np

from .models import Airports, init_db, load_joblib, load_data

def load_airports():
    init_db()
    return Airports.query.all()

def predict(origin_iata, dest_iata, date, time, departed, carrier):

    if departed == "True/":
        model = load_joblib('lr_past_departed.sav')
        meta  = load_joblib('meta_past_departed.pkl')
        score = load_joblib('score_lr_past_departed.pkl')
        df = load_data('past_train_df_departed.csv')
    else:
        model = load_joblib('lr_past_.sav')
        meta  = load_joblib('meta_past_.pkl')
        score = load_joblib('score_lr_past_.pkl')
        df = load_data('past_train_df_.csv')
    lg.warning(departed == "True/")
    input_columns = meta
    rmse_score_test = score['rmse_score_test']

    # prepare a new input vector
    input_vector = np.zeros(len(input_columns))
    time_period = 400
    date_pd = pd.to_datetime(date, format="%Y-%m-%d")
    time_split = time.split(":")
    time_int = int("".join(time_split))
    time_index = int(time_int/time_period)

    # Monday is 1 but pandas delivers Monday = 0
    dayofweek = date_pd.dayofweek + 1
    dayofmonth = date_pd.day

    time_features = [ "DEP_TIME_NIGHT", "DEP_TIME_TWILIGHT", "DEP_TIME_MORNING","DEP_TIME_NOON","DEP_TIME_AFTERNOON", "DEP_TIME_EVENING"]
    delay_features = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY', 'DEP_DELAY','ARR_DELAY']
    lg.warning(departed)
    # core core_features
    input_vector[input_columns["DAY_OF_MONTH"]] = int(dayofmonth)
    input_vector[input_columns["DAY_OF_WEEK"]] = int(dayofweek)

    try:
        input_vector[input_columns[str(time_features[time_index])]] = 1
    except:
        pass

    try:
        input_vector[input_columns['CARRIER_'+str(carrier)]] = 1
    except:
        pass

    df_delay = df[(df.ORIGIN==str(origin_iata)) & (df.DEST==str(dest_iata))]
    input_vector[input_columns['ORIGIN_DEGREE']] = int(df_delay['ORIGIN_DEGREE'])
    input_vector[input_columns['DEST_DEGREE']] = int(df_delay['DEST_DEGREE'])

    for feature in delay_features:
        input_vector[input_columns['MEDIAN_'+ feature]] = df_delay['MEDIAN_'+ feature]
        input_vector[input_columns['MEAN_'+ feature]] = df_delay['MEAN_'+ feature]
        input_vector[input_columns['Q0_'+ feature]] = df_delay['Q0_'+ feature]
        input_vector[input_columns['Q1_'+ feature]] = df_delay['Q1_'+ feature]
        input_vector[input_columns['Q3_'+ feature]] = df_delay['Q3_'+ feature]
        input_vector[input_columns['Q95_'+ feature]] = df_delay['Q95_'+ feature]

        if departed =="True/" and feature != "ARR_DELAY":
            input_vector[input_columns[feature]] = df_delay[feature]

    # prediction
    y_pred = model.predict(input_vector.reshape(1, -1))

    return y_pred, rmse_score_test
    #prediction = model.predict()
