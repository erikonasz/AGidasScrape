import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json
from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.get("https://autogidas.lt/en/skelbimai/automobiliai/porsche/")

soup = BeautifulSoup(driver.page_source, 'html.parser')

cars = []


total_cars = 0
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cars_on_page = soup.find_all('article', class_='list-item')

    for car in cars_on_page:
        title = car.find('h2', class_='item-title').text
        price = car.find('div', class_='item-price').text
        cars.append({'title': title, 'price': price})
        total_cars += 1
    next_page_button = driver.find_elements(By.XPATH, ("//a[@class='next']"))
    if not next_page_button:
        break
    else:
        next_page_button[0].click()
        time.sleep(3)
    print(len(cars))

print("Total number of cars: ", len(cars))
