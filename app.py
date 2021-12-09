import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Access the SQLite database/allows us to access and query our SQLite database file.
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes.
Base = automap_base()

#Reflect on the tables
Base.prepare(engine, reflect=True)

#With the database reflected, we can save our references to each table.
#create a variable for each of the classes so  we can reference them later,
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

#define our app for our Flask application
app = Flask(__name__)

# A. The Welcome Route
#1. Create the root, or welcome route
#The forward slash inside of the app.route denotes that we want 
# to put our data at the root of our routes
# 2. create a function welcome() with a return statement.
# 3.add the precipitation, stations, tobs, and temp routes 
#   that we'll need for this module into our return statement. 
#   We'll use f-strings to display them
#   When creating routes, we follow the naming convention /api/v1.0/
#   followed by the name of the route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

    # B. The Precipitation Route
    #-create the route/define the route and route name
    #-create the precipitation() function.
    #-add the line of code that calculates the date one year ago from the most 
    # recent date in the database
    #-write a query to get the date and precipitation for the previous year.
    # .\ signifies that we want our query to continue on the next line
    #-create a dictionary with the date as the key and the precipitation as the value by "jsonify" our dictionary.
    #-Jsonify() is a function that converts the dictionary to a JSON file.
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

    # C. The Stations Route
    #-create a new function called stations()
    #-create a query that will allow us to get all of the stations in our database
    #-unraveling our results into a one-dimensional array,use the function np.ravel(), with results as our parameter.
    #-convert our unraveled results into a list uing the list function list()
    #-jsonify the list and return it as JSON
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

    # D. Monthly Temperature Route
    #-#-create the route/define the route and route name
    #- create a function called temp_monthly()
    #- calculate the date one year ago from the last date in the database
    #-query the primary station for all the temperature observations from the previous year
    #- unravel the results into a one-dimensional array and convert that array into a list.
    #-  jsonify the list
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

     # E. Statistics Route
     #-report on the minimum, average, and maximum temperatures
     #- Should provide both a starting and ending date.
     #-Create the routes
     #-create a function called stats()
     #-add a start parameter and an end
     #-create a query to select the minimum, average, and maximum temperatures from our SQLite database
     #-Do by creating a list called sel.....*sel ndicate  multiple results for our query: minimum, average, and maximum temperatures.
     #-add an if-not statement to determine the starting and ending dat
     #-enter any date in the dataset as a start and end date to the address in your web browser:/api/v1.0/temp/2017-06-01/2017-06-30
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)










