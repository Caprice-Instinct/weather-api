from flask import Flask, render_template

# Create website object instance
app = Flask(__name__)


# @ symbol means that line is a decorator; connects that method to function
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    temperature = 23
    return {"station": station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)