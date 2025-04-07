from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set the path to your chromedriver.exe
driver_path = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Set up Chrome options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Create the driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Go to ESPN Cricinfo ILT20 2024/25 batting records page
url = "https://www.espncricinfo.com/records/tournament/batting-most-runs-career/international-league-t20-2024-25-16859"
driver.get(url)

# Wait for the page's JS to fully load
WebDriverWait(driver, 60).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# Wait for the table to load
WebDriverWait(driver, 60).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "table.ds-w-full.ds-table"))
)
print("✅ Table loaded successfully.")

# Extract headers using JavaScript (if dynamically loaded)
headers = driver.execute_script("""
    var table = document.querySelector('table.ds-w-full.ds-table');
    var headers = [];
    var thElements = table.querySelectorAll('thead th');
    thElements.forEach(function(th) {
        headers.push(th.innerText.trim());
    });
    return headers;
""")

print(f"Headers: {headers}")  # Debugging: Print headers

# Scrape the table rows
table = driver.find_element(By.CSS_SELECTOR, "table.ds-w-full.ds-table")
rows = table.find_elements(By.TAG_NAME, "tr")

# Extract data rows
data = []
for row in rows[1:]:
    cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
    
    # Ensure the row has the correct number of columns
    if len(cols) == len(headers):
        data.append(cols)
    else:
        print(f"Skipping row with incorrect column count: {cols}")  # Debugging

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)

# Show preview
print(f"Data preview:\n{df.head()}")  # Debugging step

# Save to CSV
df.to_csv("ilt20_batting_stats_2024.csv", index=False)
print("✅ Data saved to ilt20_batting_stats_2024.csv")

# Close the driver
driver.quit()
print("✅ Web driver closed.")  # Final confirmation
