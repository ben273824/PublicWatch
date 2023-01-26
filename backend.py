from flask import Flask, render_template, request, session, redirect, url_for
from SenateStocks import getTrades
import pandas as pd

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        startDate = request.form.get("startDate")
        startDate = "{}/{}/{}".format(startDate[5:7], startDate[-2:], startDate[:4])
        endDate = request.form.get("endDate")
        endDate = "{}/{}/{}".format(endDate[5:7], endDate[-2:], endDate[:4])
        stocks = getTrades(startDate, endDate, fname, lname)
        length = len(stocks)
        session['startDate'] = startDate
        session['endDate']= endDate
        session['fname']= fname
        session['lname']= lname
        session['stocks']= stocks.to_json()
        session["length"] = length
        return redirect(url_for("data"))
    elif session.get("stocks"):
        return render_template("index.html", submit=True)
    return render_template("index.html", submit=False)

@app.route("/sources")
def sources():
    return render_template("sources.html")


@app.route("/data")
def data():
    if session.get("stocks"):
        return render_template("data.html", startDate=session['startDate'], endDate=session['endDate'],
        fname = session["fname"], lname=session["lname"], stocks=pd.read_json(session["stocks"]), length=session["length"])
    else:
        return redirect(url_for("home"))

app.debug = True
app.secret_key = "aidjasdijasldj"
app.run()