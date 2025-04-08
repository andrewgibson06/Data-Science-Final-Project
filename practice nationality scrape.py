import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

#imports the batting csv file
csv_file_path = "ilt20_batting_stats_2025.csv"
df = pd.read_csv(csv_file_path)

#check that the player url is there
if "Player Profile URL" not in df.columns:
    raise ValueError("Player Profile URL column not found in the CSV file.")

#adds the nationality column into the dataframe
df["Nationality"] = None

#sets up the driver path and options
service = Service("C:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

#identifies the url to scrape (in this case a practice url)
for index, row in df.iterrows():
    url = row["Player Profile URL"]
    driver.get(url)

    #web scrape begins
    try:
        nationality_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='ds-text-title-l ds-font-bold']/following-sibling::div/span[@class='ds-text-comfortable-s'][1]")))
        df.at[index, "Nationality"] = nationality_data.text
        print(f"[{index+1}] Nationality for {row['Player Profile URL']}: {nationality_data.text}")

    except Exception as e:
        print(f"[{index+1}] Could not find nationality for {url}: {e}")

    time.sleep(random.uniform(20, 45))


driver.quit()

output_file = "ilt20_batting_stats_with_nationality_2025.csv"
df.to_csv(output_file, index=False)
print(f"Saved updated CSV to: {output_file}")
