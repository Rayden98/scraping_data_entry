from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import requests

form = "https://docs.google.com/forms/d/e/1FAIpQLSfXpq66XJ0_4wI9CndFqPvIJIFITq0v3N1kpQhBBy2CItAsPA/viewform?usp=sf_link"
data = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.68120802832031%2C%22east%22%3A-122.25823439550781%2C%22south%22%3A37.71909675140249%2C%22north%22%3A37.86289163942171%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}
list_link_address = []
list_price_tag = []
list_address = []
apartments = {}

response = requests.get(data, headers=headers)
web_page = response.text


soup = BeautifulSoup(web_page, "html.parser")

link_address = soup.find_all(name="a", class_="StyledPropertyCardDataArea-c11n-8-89-0__sc-yipmu-0")

for each in link_address:
    list_link_address.append(each.get("href"))

price_tag = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1")

for each in price_tag:
    price = each.text.split("+")[0]
    list_price_tag.append((price))

address = soup.find_all(name="address")

for each in address:
    list_address.append((each.text))

for n in range(len(list_price_tag)):
    apartments[n] = {
        "price": list_price_tag[n],
        "address": list_address[n],
        "link": list_link_address[n],
    }

print(apartments)

for n in range(0, len(apartments)):
    s = Service('C:/Users/MINED/Documents/Programs/chromedriver.exe')

    driver = webdriver.Chrome(service=s)
    driver.get(form)
    time.sleep(5)

    address = driver.find_element(By.CLASS_NAME, "KHxj8b")
    address.send_keys(f'{apartments[n]["address"]}')

    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea')
    price.send_keys(f'{apartments[n]["price"]}')

    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]/textarea')
    link.send_keys(f'{apartments[n]["link"]}')

    button_send = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    button_send.click()
    time.sleep(4)

    driver.quit()