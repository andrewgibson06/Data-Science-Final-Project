from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#sets up the driver path and options
service = Service("C:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

#identifies the url to scrape (in this case a practice url)
url = "https://www.espncricinfo.com/cricketers/shai-hope-581379"
driver.get(url)

#web scrape begins
try:
    nationality = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='ds-text-title-l ds-font-bold']/following-sibling::div/span[@class='ds-text-comfortable-s'][1]")))
    print("Player's country:", nationality.text)

except Exception as e:
    print("Could not find the player's country.")
    print("Error:", e)

finally:
    driver.quit()
