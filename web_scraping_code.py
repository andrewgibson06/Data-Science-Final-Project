from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set the path to your chromedriver.exe
driver_path = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Set up Chrome options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Create the driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Go to the target URL
url = "https://www.espncricinfo.com/records/tournament/batting-most-runs-career/international-league-t20-2024-25-16859"
driver.get(url)

# Wait for page to load fully
WebDriverWait(driver, 60).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# Wait for the actual table to be present
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.ds-w-full.ds-table"))
)
print("✅ Table loaded successfully.")

# --- GET HEADERS ---
header_spans = driver.find_elements(By.CSS_SELECTOR, "thead td span")
headers = [h.text.strip() for h in header_spans if h.text.strip() != ""]

print(f"Headers: {headers}")

# --- GET ROW DATA ---
rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
data = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text.strip() for col in cols]
    if len(row_data) == len(headers):
        data.append(row_data)
    else:
        print(f"Skipping row with incorrect column count: {row_data}")

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)
print(df.head())

# Save to CSV
df.to_csv("ilt20_batting_stats_2024.csv", index=False)
print("✅ Data saved successfully!")

# Quit browser
driver.quit()
print("✅ Web driver closed.")

