from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # optional: don't open a window
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# Start URL (you can change filters as needed)
url = "https://www.olx.uz/oz/nedvizhimost/doma/prodazha/?currency=UZS&page=2&search%5Bfilter_enum_location%5D%5B0%5D=1&search%5Bfilter_enum_private_house_type%5D%5B0%5D=1&search%5Bfilter_enum_private_house_type%5D%5B1%5D=5"

# Store results
all_listings = []

# Loop through pages
while True:
    driver.get(url)
    time.sleep(2)  # wait for JS to load content

    # Parse page source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # --- Find listings on the current page ---
    listings = soup.find_all("div", class_="css-1sw7q4x")  # You may need to inspect actual class name

    for item in listings:
        title = item.find("span", class_="css-6as4g5")
        price = item.find("p", class_="css-uj7mm0")
        address = item.find("p", class_="css-vbz67q")
        is_featured = item.find("p", class_="css-vbz67q")

        all_listings.append({
            "title": title.get_text(strip=True) if title else "",
            "price": price.get_text(strip=True) if price else "",
            "address": address.get_text(strip=True) if address else ""
        })

    # --- Try to click "Next" button ---
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="pagination-forward"]')
        url = next_button.get_attribute("href")
        if not url:
            break
    except:
        print("No more pages.")
        break

# Append or create data
file_path = '../data/domuz_listings.csv'
new_data = pd.DataFrame(all_listings)

if os.path.exists(file_path):
    old_data = pd.read_csv(file_path)

    # Combine and remove duplicates (based on square + price + address)
    combined = pd.concat([old_data, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=["square", "price", "address"])

    # Save back to the same file
    combined.to_csv(file_path, index=False, encoding='utf-8-sig')
else:
    new_data.to_csv(file_path, index=False, encoding='utf-8-sig')
print(new_data.head())

# Close driver
driver.quit()
