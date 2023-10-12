import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from flask import Flask, request, render_template
import numpy as np
import pickle

#################################################
# Database Setup
#################################################

# Create a reference to the file 
database_path = Path("flaskDB.sqlite")

# Create Engine
engine = create_engine(f"sqlite:///{database_path}")
conn = engine.connect()

# Query All Records in the the Database
loan_details = pd.read_sql("SELECT * FROM flaskDB", conn)

#################################################
# Flask Setup
#################################################

# create Flask app
app = Flask(__name__)

# load pickel model
model = pickle.load(open('trained_model_v2.sav', 'rb'))

@app.route("/")
def Welcome():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]

    prediction = model.predict(features)
    return render_template("index.html", prediction_text ="the Loan Amount code {}. \n If Code is 0 , Client likely to NOT DEFAULT \n If Code = 1, Client is like to default, Proceed with caution". format(prediction))

@app.route("/data")
def loan_data():
   
    return loan_details.to_json()

if __name__ == "__main__":
    app.run(debug=True)