from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time

CHROME_DRIVER_PATH = "\D:\Development\chromedriver.exe"
chromedriver_autoinstaller.install()
service = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


###################### WEBSCRAPING ZILLOW PAGE AND FORMING LISTS FOR LINKS/ADDRESSES/PRICES ############################
LISTINGS_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
response = requests.get(url=LISTINGS_URL, headers=header)
zillow_wp = response.text
soup = BeautifulSoup(zillow_wp, "html.parser")


all_link_elements = soup.select(".property-card-data a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    # print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
print(all_links)

addresses = soup.find_all(name="address")

all_addresses = []
for address in addresses:
    address_text = address.getText()
    all_addresses.append(address_text)
print(all_addresses)

rents = soup.find_all(class_="bqsBln")
# print(rents)

all_rent = []
for rent in rents:
    rent_text = rent.getText()
    # print(rent_text)
    all_rent.append(rent_text)
print(all_rent)

############################################### SELENIUM ###############################################################

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdkDEkjE4Q0fA5AS7Gou-pHrtR2SZGn6IjGd-rc0GryJxlATQ/viewform?usp=sf_link"

driver = webdriver.Chrome(service=service, options=options)

driver.get(FORM_URL)
driver.fullscreen_window()
time.sleep(2)

for listing in range(len(all_addresses)):
    addy_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    addy_input.send_keys(all_addresses[listing])

    rent_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    rent_input.send_keys(all_rent[listing])

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(all_links[listing])

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()
    time.sleep(2)

    another_one = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_one.click()
    time.sleep(2)