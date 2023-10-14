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
database_path = Path("Resources/flaskDB.sqlite")

# Create Engine
engine = create_engine(f"sqlite:///{database_path}")
conn = engine.connect()

# Query All Records in the the Database
loan_details = pd.read_sql("SELECT * FROM flaskDB", conn)

# List the uniques states
states_unique = sorted(loan_details['State'].unique())

#################################################
# Flask Setup
#################################################

# create Flask app
app = Flask(__name__)

# load pickel model
model = pickle.load(open('trained_model_v3.sav', 'rb'))


@app.route("/")
def Welcome():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]

    prediction = model.predict(features)
    return render_template("index.html", prediction_text="the Loan Amount code {}. \n If Code is 0 , Client likely to NOT DEFAULT \n If Code = 1, Client is like to default, Proceed with caution". format(prediction))


@app.route("/graphs", methods=["GET"])
def graphs():
    return render_template('index_data.html', states_unique=states_unique)


@app.route("/data")
def data():
    # Filter data for ChargedOff records only
    charged_off = loan_details[loan_details['MIS_Status'] == 1]
    # Create a dictionary that stores yearly trend for each state
    graph_data = {}
    for state in states_unique:
        charged_off_state = charged_off[charged_off['State'] == state]
        # Process data for the timeline
        year_count = charged_off_state['ApprovalFY'].value_counts(
        ).sort_index()
        # Process data for the barchart
        year_median_amount = charged_off_state.groupby(
            'ApprovalFY')['ChgOffPrinGr'].median().sort_index()
        # Conbine 2 sets of data
        year_data = pd.concat([year_median_amount, year_count], axis=1).rename(columns={'ChgOffPrinGr': 'MedianChargedOffAmount',
                                                                                        'ApprovalFY': 'RecordCount'}).to_dict()
        graph_data[state] = year_data
    return graph_data


if __name__ == "__main__":
    app.run(debug=True)
