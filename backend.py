from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
from SenateStocks import getTrades
from yahooFinance import analyzeTrade
import pandas as pd
import json

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    model, x, y = analyzeTrade(year, month, day, ticker)
    data = []
    for j in range(len(y)):
        dict = {"x":j, "y":y.iloc[j]}
        data.append(dict)
    return render_template("analysis.html", points=data, length=len(data), tradeDay = x,
    tradeDate = "{}-{}-{}".format(year, month, day), name = stocks["FirstName"][i] + " " + stocks["LastName"][i], 
    type=stocks["TransactionType"][i], ticker=ticker, model= model)



app.debug = True
app.secret_key = "aidjasdijasldj"
app.run()