import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.get("https://autogidas.lt/en/skelbimai/automobiliai/porsche/")

soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(4)
accept_cookies = driver.find_element(By.XPATH, '//button[text()="I Accept"]')
accept_cookies.click()
time.sleep(3)

cars = []
total_cars = 0

while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    allcars = soup.find_all('article', class_='list-item')

    for car in allcars:
        title = car.find('h2', class_='item-title').text
        price = car.find('div', class_='item-price').text
        cars.append({'title': title, 'price': price})
        total_cars += 1
    next_page_button = driver.find_elements(By.XPATH, ("//div[@class='next-page-inner']"))
    if not next_page_button:
        break
    else:
        next_page_button[0].click()
        time.sleep(3)

print("Total number of cars: ", len(cars))
print("Cars list: ", cars)

with open('cars.csv', mode='w', newline='') as csv_file:
    fieldnames = ['title', 'price']
    wrt = csv.DictWriter(csv_file, fieldnames=fieldnames)
    wrt.writeheader()

    for car in cars:
        car['title'] = car['title'].strip()
        car['title'] = car['title'].strip()
        wrt.writerow(car)
