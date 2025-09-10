import os
import pandas as pd
import analytics
import model
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from dotenv import load_dotenv
from ucimlrepo import fetch_ucirepo 
import pickle
import numpy as np

load_dotenv()
app = Flask(__name__)

# Connessione al DB
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

@app.route("/")
def home():
    return "🚴 Bike Sharing Flask App attiva!"

@app.route("/load-data", methods=["POST"])
def load_data():
    bike_sharing = fetch_ucirepo(id=275) 
    # data (as pandas dataframes) 
    X = bike_sharing.data.features 
    y = bike_sharing.data.targets  
    bike_sharing_dataframe = bike_sharing.data['original']
    bike_sharing_dataframe.to_sql("bike_sharing", engine, if_exists="append", index=False)
    return jsonify({"message": "Dataset caricato con successo!"})

def download_data():
    # Recupera il dataset dal database
    df = pd.read_sql("SELECT * FROM bike_sharing", engine)
    return df

@app.route("/records")
def records():
    query = "SELECT * FROM bike_sharing LIMIT 10;"
    result = pd.read_sql(query, engine)
    return result.to_json(orient="records")

@app.route("/train_model")
def train_model():
    df = download_data()
    model.train_model(df)
    return jsonify({"message": "Model allenato con successo!"})

@app.route("/prediction", methods=["POST"])
def prediction():
    # Caricamento
    with open("final_model.pkl", "rb") as f:
        loaded_model = pickle.load(f)

    try:
        # 1. Recupera i parametri dal body JSON
        input_data = request.get_json()
        # 2. Trasformiamo in DataFrame (anche una singola riga)
        bike_sharing_dataframe = pd.DataFrame([input_data])
        bike_sharing_dataframe["hour_sin"] = np.sin(2 * np.pi * bike_sharing_dataframe["hr"]/24)
        bike_sharing_dataframe["hour_cos"] = np.cos(2 * np.pi * bike_sharing_dataframe["hr"]/24)
        # Rimuovere le colonne originali
        bike_sharing_dataframe.drop("hr",axis=1,inplace=True)
    
        bike_sharing_dataframe["month_sin"] = np.sin(2 * np.pi * bike_sharing_dataframe["mnth"]/12)
        bike_sharing_dataframe["month_cos"] = np.cos(2 * np.pi * bike_sharing_dataframe["mnth"]/12)
        # Rimuovere le colonne originali
        bike_sharing_dataframe.drop("mnth",axis=1,inplace=True)
        # 3. Predizione
        print(list(bike_sharing_dataframe.columns))
        cols = list(bike_sharing_dataframe.columns)  # prendi tutte le colonne
        cols.remove('avg_temp')           # rimuovi avg_temp dalla lista
        cols.append('avg_temp')           # aggiungi avg_temp alla fine
        bike_sharing_dataframe = bike_sharing_dataframe[cols]  # riordina il DataFrame

        prediction = loaded_model.predict(bike_sharing_dataframe)
        # 4. Risposta JSON
        return jsonify({"prediction": float(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route("/analytics/hourly")
def hourly_plot():
    df = download_data()
    return analytics.hourly_plot(df)

@app.route("/analytics/weekday")
def weekday_plot():
    df = download_data()
    return analytics.weekday_plot(df)

@app.route("/analytics/monthly")
def monthly_plot():
    df = download_data()
    return analytics.month_plot(df)

@app.route("/analytics/casual-vs-registered")
def casual_registered_plot():
    df = download_data()
    return analytics.distribution_casual_registered(df)

@app.route("/analytics/heatmap")
def heatmap_plot():
    df = download_data()
    return analytics.heatmap(df)

@app.route("/analytics/trend")
def trend_plot():
    df = download_data()
    return analytics.trend_weekly(df)

@app.route("/analytics/holyday")
def holyday_stats():
    df = download_data()
    return analytics.holyday_stats(df)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
