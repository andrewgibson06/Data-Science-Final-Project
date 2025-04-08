#imports the necessary libraries: selenium as the table is dynamic and pandas to save the data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import requests

#creates the path to my chromedriver which is needed to run selenium
driver_path = "C:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

#set up options for the web driver, headless mode is not used as the table loads differently in headless mode
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

#creates the web driver using the path and options
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

#loads the website
url = "https://www.espncricinfo.com/records/tournament/batting-most-runs-career/international-league-t20-2024-25-16859"
driver.get(url)

#waits for the page to load fully before running script
WebDriverWait(driver, 60).until(lambda d: d.execute_script("return document.readyState") == "complete")

#waits for the table to fully load
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.ds-w-full.ds-table")))
print("Table loaded successfully")

#identifies the headers
header_spans = driver.find_elements(By.CSS_SELECTOR, "thead td span")
headers = [h.text.strip() for h in header_spans if h.text.strip() != ""]
headers.append("Player Profile URL")
print(f"Headers: {headers}")

#identfies the rows
rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
data = []

#loops through every row and collects the data
# Inside your loop where you scrape player data:

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text.strip() for col in cols]

    if len(row_data) >= 1:
        try:
            player_elem = cols[0].find_element(By.TAG_NAME, "a")
            player_link = player_elem.get_attribute("href")
            if player_link and player_link.startswith("/cricketers"):
                # Prepending the base URL to the relative URL
                player_link = "https://www.espncricinfo.com" + player_link
        except:
            player_link = None
        
        if len(row_data) == len(headers) - 1:
            row_data.append(player_link)
            data.append(row_data)
        else:
            print(f"Skipping row due to mismatch: {row_data}")
    else:
        print("Empty row")


#quits the opened browser
driver.quit()
print("Finished initial scrape of table")

#converts the data to a dataframe
df = pd.DataFrame(data, columns=headers)
print("Initial data collection from table:\n", df.head())

#saves it to a csv file
df.to_csv("ilt20_batting_stats_2025.csv", index=False)
print("Data saved successfully")


