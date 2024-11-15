from flask import Flask, render_template
import pandas as pd


# Create website object instance
app = Flask(__name__)


stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations =stations[['STAID',"STANAME                                 "]]


# @ symbol means that line is a decorator; connects that method to function
@app.route("/")
def home():
    return render_template('home.html', data=stations.to_html())


# Route for a particular station on a particular date
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # The filename takes in the station number
    # zfill(int) method fills the missing part with zeros
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


# Gets all the data for a particular station
@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


# All data for a specific station in a particular year
@app.route("/api/v1/annual/<station>/<year>")
def yearly_data(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)

    # Converts the numbers for dates into string example: 19880101 -> '19880101'
    df['    DATE'] = df['    DATE'].astype(str)

    # Check if the year is the same as the one queried
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result

if __name__ == "__main__":
    app.run(debug=True)