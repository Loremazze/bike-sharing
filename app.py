import os
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine
from dotenv import load_dotenv

'''
env_content = """DB_USER=postgres
DB_PASSWORD=lunazoeuga16
DB_HOST=localhost
DB_PORT=5432
DB_NAME=testdatabase
"""

with open(".env", "w") as f:
    f.write(env_content)

print(".env file created!")
'''

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
    df = pd.read_csv("hour.csv", parse_dates=["dteday"])
    df.to_sql("bike_sharing", engine, if_exists="append", index=False)
    return jsonify({"message": "Dataset caricato con successo!"})

@app.route("/records")
def records():
    query = "SELECT * FROM test_table LIMIT 10;"
    result = pd.read_sql(query, engine)
    return result.to_json(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
