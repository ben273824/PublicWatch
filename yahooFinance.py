from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import statsmodels.api as sm
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os
from time import sleep
import datetime
import time

def analyzeTrade(year, month, day, ticker):
    ops = Options()
    ops.headless = True
    ops.add_argument("--width=1920")
    ops.add_argument("--height=1080")
    driver = webdriver.Firefox(options=ops, executable_path=r"C:\Users\klick\Pythonprojects\PublicWatch\node_modules\geckodriver\geckodriver.exe")
    stocks = ["SPY", ticker]
    data = pd.DataFrame()
    date = ["{}".format(year),"{}".format(month),"{}".format(day)]
    tradeDate = datetime.datetime(int(date[0]),int(date[1]), int(date[2]))
    tradeDate = int(time.mktime(tradeDate.timetuple()))
    startDate = datetime.datetime.fromtimestamp(tradeDate - 13000000).strftime("%Y-%m-%d")
    endDate = datetime.datetime.fromtimestamp(tradeDate  + 13000000).strftime("%Y-%m-%d")

    for i in range(len(stocks)):
        url = "https://finance.yahoo.com/quote/{}/history?p={}".format(stocks[i], stocks[i])
        driver.get(url)
        download = driver.find_element(By.XPATH, ".//*[text()='Download']")
        download = download.find_element(By.XPATH, "./..")
        if i == 0:
            try:
                exit = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]")))
                exit.click()
            except:
                pass
            try:
                ad = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"monalixa-finance-desktop-web-qsp-stickyfooter-seqmsg\"]/div/button")))
                ad.click()
            except:
                pass
        else:
            sleep(1)
        setDate = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div")
        setDate.click()
        setDate = driver.find_element(By.NAME, "startDate")
        setDate.click()
        setDate.send_keys("{}".format(startDate))
        setDate = driver.find_element(By.NAME, "endDate")
        setDate.click()
        setDate.send_keys("{}".format(endDate))
        button = driver.find_element(By.CSS_SELECTOR, "button.Bgc\(\$linkColor\):nth-child(1)")
        button.click()
        sleep(0.5)
        download.click()
        sleep(0.5)
        df = pd.read_csv(r"C:\Users\klick\Downloads\{}.csv".format(stocks[i]))
        returns = []
        y = df["Adj Close"]
        for j in range(1, len(y)):
            returns.append((y[j]-y[j-1])/y[j-1])
        if (i == 0):
            data["Date"] = df["Date"][1:]
        data["Returns{}".format(stocks[i])] = np.array(returns)
        os.remove(r"C:\Users\klick\Downloads\{}.csv".format(stocks[i]))

    driver.quit()

    data["Event"] = 0
    day = data.index[data["Date"] == "{}-{}-{}".format(date[0], date[1], date[2])].to_list()[0] - 1 
    data.loc[day:, "Event"] = 1

    x=data.iloc[:day, 1]
    y = data.iloc[:day, 2]
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    data["Prediction"] = model.predict(sm.add_constant(data.iloc[:, 1]))
    data["Residuals"] = data.iloc[:,2] - data["Prediction"]
    data["CumulativeResiduals"] = data["Residuals"].cumsum()
    model = sm.OLS(data["CumulativeResiduals"], sm.add_constant(data["Event"])).fit()

    return model, day, data["CumulativeResiduals"]
