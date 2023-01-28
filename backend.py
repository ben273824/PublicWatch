from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from SenateStocks import getTrades
from yahooFinance import analyzeTrade
import pandas as pd
import json

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

@app.route("/analysis/<i>")
def analysis(i):
    i = int(i)
    stocks = pd.read_json(session["stocks"])
    year = stocks["TransactionDate"][i][-4:]
    month = stocks["TransactionDate"][i][:2]
    day = stocks["TransactionDate"][i][3:5]
    ticker = stocks["Ticker"][i]
    summary, x, y = analyzeTrade(year, month, day, ticker)
    data = []
    for i in range(len(y)):
        dict = {"x":i, "y":y.iloc[i]}
        data.append(dict)
    return render_template("analysis.html", points=data, length=len(data))



app.debug = True
app.secret_key = "aidjasdijasldj"
app.run()