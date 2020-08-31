import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes :<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/start'>start</a><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Calculate the date 1 year ago from the last data point in the database"""
    # Query all 
    date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).order_by(Measurement.date).all()

    session.close()

    # Create a dictionary with date and precipitation data
    yr_rain = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        yr_rain.append(precipitation_dict)
    
    return jsonify(yr_rain)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()
    # print(results)
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)  


  
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Choose the station with the highest number of temperature observations.
    date = dt.datetime(2016, 8, 17)
   
    temp_count = session.query(Measurement.tobs).filter(Measurement.date > date).filter(Measurement.station == 'USC00519281').all()

    session.close()
   
    # Convert list of tuples into normal list
    tobs = list(np.ravel(temp_count))

    return jsonify(tobs)  





if __name__ == '__main__':
    app.run(debug=True)     