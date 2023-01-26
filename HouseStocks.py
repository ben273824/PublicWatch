from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

ops = Options()
ops.headless = True
ops.binary_location = "/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox"
serv = Service("/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=serv, options=ops)



def getYear(year):
    url = "https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure#Search"
    driver.get(url)
    sleep(1)
    select = driver.find_element(By.ID, "FilingYear")
    select = Select(select)
    select.select_by_visible_text("{}".format(year))
    enter = driver.find_element(By.XPATH, "/html/body/section/div/div[2]/div[6]/div[3]/div[2]/div/div[1]/form/div[4]/button[1]")
    enter.click()
    sleep(1)
    numpages = int(driver.find_elements(By.CLASS_NAME, "paginate_button")[-2].text)
    for i in range(1, numpages-3):
        try:
            page = driver.find_elements(By.CLASS_NAME, "paginate_button")[i]
            page.click()
        except:
            page = driver.find_elements(By.CLASS_NAME, "paginate_button")[4]
            page.click()
        sleep(1)
        table = driver.find_element(By.TAG_NAME, "tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for j in range(len(rows)):
            file = rows[j].find_elements(By.TAG_NAME, "td")
            if file[3].text == "PTR Original":
                file[0].click()
                input()
    page = driver.find_elements(By.CLASS_NAME, "paginate_button")[5]
    page.click()
    page = driver.find_elements(By.CLASS_NAME, "paginate_button")[6]
    page.click()

        
    

getYear(2020)
