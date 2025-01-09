from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from inputs import betName

# change below variables according to decision of interest
bet_name = betName #As per url not title in UI
bet_id = 1735446659488

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Open the URL
url = "https://polymarket.com/event/"+bet_name+"?tid=1735443980938"

# Load the webpage
driver.get(url)

# Wait for dynamic elements to load
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-goNzNd')))

# Parse the rendered page with BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract elements
probabilities = soup.find_all('p', class_='c-dqzIym c-dqzIym-fxyRaa-color-normal c-dqzIym-cTvRMP-spacing-normal c-dqzIym-iIobgq-weight-medium c-dqzIym-icEtPXM-css')
decisions = soup.find_all('p', class_='c-cZBbTr')

# Store data of each rate change decision and their respective probabilities
data = {}
for i, prob in enumerate(probabilities):
    data[decisions[i].text] = prob.text

# Binary odds of a rate change vs rates remaining the same
polyOddsForNoChange = int(data['No Change'][:-1])
polyOddsForChange = 100 - polyOddsForNoChange

driver.quit()

