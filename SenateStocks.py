from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
import pandas as pd
import re


def search(driver, startD, endD, first = "", last = ""):
    url = "https://efdsearch.senate.gov/search/home/"
    driver.get(url)
    agree = driver.find_element(By.ID, "agree_statement")
    agree.click()   
    driver.find_elements(By.ID, "reportTypes")[1].click()
    name = driver.find_element(By.ID, "firstName")
    name.send_keys(first)
    name = driver.find_element(By.ID, "lastName")
    name.send_keys(last)
    date = driver.find_element(By.ID, "fromDate")
    date.send_keys(startD)
    date = driver.find_element(By.ID, "toDate")
    date.send_keys(endD)
    submit = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/div/button")
    submit.click()
    sleep(1)

def scrape(driver, stocks):
    length = driver.find_element(By.ID, "filedReports_info").text
    try:
        length = int(re.findall("Showing 1 to \d+ of (\d+) entries", length)[0])
    except:
        length = 0

    handle = driver.current_window_handle

    while length>0:
        table = driver.find_element(By.XPATH, "//*[@id=\"filedReports\"]/tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for i in range(len(rows)):
            try:
                link = rows[i].find_element(By.TAG_NAME, "a")
            except:
                continue
            first = rows[i].find_elements(By.TAG_NAME, "td")[0].text
            last = rows[i].find_elements(By.TAG_NAME, "td")[1].text
            link.click()
            sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            try:
                data = driver.find_element(By.TAG_NAME, "tbody")
            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue
            data= data.find_elements(By.TAG_NAME, "tr")
            for row in data:
                stocksRow = [last, first]
                columns = row.find_elements(By.TAG_NAME, "td")
                for j in range(1, len(columns)):
                    stocksRow.append(columns[j].text)
                stocks.loc[len(stocks.index)] = stocksRow
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        length -= 25
        if length <= 0:
            break
        else:
            driver.find_element(By.ID, "filedReports_next").click()
            sleep(1)
    

    driver.quit()

def getTrades(startD, endD, first = "", last = ""):
    
    
    ops = Options()
    ops.headless = True
    driver = webdriver.Firefox(options=ops, executable_path=r"C:\Users\klick\Pythonprojects\PublicWatch\node_modules\geckodriver\geckodriver.exe")


    stocks = pd.DataFrame(columns=["LastName", "FirstName", "TransactionDate", "Owner", "Ticker", 
    "AssetName", "AssetType", "TransactionType", "Amount", "Comment"])

    search(driver, startD, endD, first, last)
    scrape(driver, stocks)
    return stocks












