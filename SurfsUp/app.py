# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify
import pandas as pd
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start><br/>"
        f"/api/v1.0/start_date/<start>/end_date/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Load the DataFrame from the CSV file
    prec_df = pd.read_csv('outputs/precipitation_data.csv')
    
    # Convert the DataFrame to a dictionary
    precipitation_dict = prec_df.set_index('date')['precipitation'].to_dict()

    # Convert the dictionary to JSON
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Load the DataFrame from the CSV file
    stations_df = pd.read_csv('Resources/hawaii_stations.csv')

    # Convert the DataFrame to a dictionary
    stations_dict = stations_df.to_dict(orient='records')

    # Convert the dictionary to JSON
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # Load the DataFrame from the CSV file
    most_active_df = pd.read_csv('outputs/temp_obs.csv')

    # Convert the DataFrame to a dictionary
    most_active_dict = most_active_df.set_index('date')['temperature observed'].to_dict()

    # Convert the dictionary to JSON
    return jsonify(most_active_dict)

@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
    # Load the DataFrame from the CSV file
    most_active_df = pd.read_csv('outputs/temp_obs.csv')
    
    # Convert the 'date' column to datetime format
    most_active_df['date'] = pd.to_datetime(most_active_df['date'])

    # Convert 'start' to datetime format
    start_date = pd.to_datetime(start)
    
    # Filter the DataFrame based on the start date
    mas_filtered_df = most_active_df[most_active_df['date'] >= start_date]

    # Calculate the minimum temperature, average temperature, and maximum temperature
    min_val = mas_filtered_df['temperature observed'].min()
    avg_val = mas_filtered_df['temperature observed'].mean()
    max_val = mas_filtered_df['temperature observed'].max()
    
    # Create a dictionary to include the min, average, and max temperatures
    results_dict = {'min': min_val, 'average': avg_val, 'max': max_val}

    # Convert the dictionary to JSON
    return jsonify(results_dict)

@app.route("/api/v1.0/start_date/<start>/end_date/<end>")
def start_and_end(start,end):
    # Load the DataFrame from the CSV file
    most_active_df = pd.read_csv('outputs/temp_obs.csv')
    
    # Convert the 'date' column to datetime format
    most_active_df['date'] = pd.to_datetime(most_active_df['date'])

    # Convert 'start' and 'end' to datetime format
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    
    # Filter the DataFrame based on the start date and end date
    mas_filtered_df = most_active_df[(most_active_df['date'] >= start_date) & (most_active_df['date'] <= end_date)]

    # Calculate the minimum temperature, average temperature, and maximum temperature
    min_val = mas_filtered_df['temperature observed'].min()
    avg_val = mas_filtered_df['temperature observed'].mean()
    max_val = mas_filtered_df['temperature observed'].max()

    # Create a dictionary to include the min, average, and max temperatures
    results_dict = {'min': min_val, 'average': avg_val, 'max': max_val}

    # Convert the dictionary to JSON
    return jsonify(results_dict)

if __name__ == "__main__":
    app.run(debug=True)