#import libraries
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

#undetected chromedriver is used as other software is detected by the website and blocked pages from loading
import undetected_chromedriver as uc

#imports the batting csv file
csv_file_path = "ilt20_batting_stats_2025.csv"
df = pd.read_csv(csv_file_path)

#check that the player url is there
if "Player Profile URL" not in df.columns:
    raise ValueError("Player Profile URL column not found in the CSV file.")

#adds the nationality column into the dataframe
df["Nationality"] = None

#sets up the undetected chromedriver
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
driver = uc.Chrome(options=options)

#opens a new tab
driver.get("about:blank")

#identifies the url to scrape from the csv file
for index, row in df.iterrows():
    url = row["Player Profile URL"]

    try:
        #opens a new tab to make it seem less like a bot
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)

        #waits for the nationality to load in
        nationality_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='ds-text-title-l ds-font-bold']/following-sibling::div/span[@class='ds-text-comfortable-s'][1]")))
        df.at[index, "Nationality"] = nationality_data.text
        print(f"[{index+1}] Nationality for {url}: {nationality_data.text}")

    except Exception as e:
        print(f"[{index+1}] Could not get data for {url}: {e}")

    finally:
        #closes the opened tab and switches back to the main tab
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        #waits a random time to avoid being blocked
        time.sleep(random.uniform(20, 45))

driver.quit()

#saves the data to a new file
output_file = "ilt20_batting_stats_with_nationality_2025.csv"
df.to_csv(output_file, index=False)
print(f"Saved updated CSV to: {output_file}")
