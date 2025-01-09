import requests
from inputs import currentRateRange, dateTime
from bs4 import BeautifulSoup

URL = "https://www.investing.com/central-banks/fed-rate-monitor"
page = requests.get(URL)
text = page.text

soup = BeautifulSoup(page.content, "html.parser")

# Find all meeting times (dates)
dates = []
info_blocks = soup.find_all('div', class_='infoFed')

for block in info_blocks:
    # Extract the meeting date (e.g., "Jan 29, 2025 02:00PM ET")
    date = block.find('i').text.strip()
    dates.append(date)

# Find all rate probability items
rate_probabilities = []
rate_sections = soup.find_all('div', class_='percfedRateWrap')

for i, section in enumerate(rate_sections):
    # Get the date corresponding to this section
    meeting_date = dates[i] if i < len(dates) else 'Unknown Date'

    # Extract rate probabilities for the given section
    rate_items = section.find_all('div', class_='percfedRateItem')

    for item in rate_items:
        # Extract rate range (e.g., "4.25 - 4.50")
        rate_range = item.find('span').text.strip()

        # Extract probability (e.g., "91.1%")
        probability = item.find_all('span')[-1].text.strip()

        # Append to the list as a tuple
        rate_probabilities.append((meeting_date, rate_range, probability))

# Store results
bondOddsToChange = -1
for date, rate, prob in rate_probabilities:
    if rate == currentRateRange and date == dateTime:
        bondOddsForNoChange = float(prob[:-1])
        break

if bondOddsForNoChange == -1: print('Error scraping bond implied odds')


