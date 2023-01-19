import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

def get_cars(url):
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(4)
    accept_cookies = driver.find_element(By.XPATH, '//button[text()="I Accept"]')
    accept_cookies.click()
    time.sleep(3)

    cars = []
    counter = 0

    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        allcars = soup.find_all('article', class_='list-item')

        for car in allcars:
            title = car.find('h2', class_='item-title').text
            price = car.find('div', class_='item-price').text
            description = car.find('div', class_='item-description').text
            description_list = description.split(',')

            liter = description_list[0].strip()
            fuel_type = description_list[1].strip()
            year = description_list[2].strip()
            transmission = description_list[3].strip()
            try:
                engine = description_list[4].strip()
            except:
                print("Engine info (4 list) not found.")

            cars.append({'title': title, 'price': price, 'liter': liter, 'fuel_type': fuel_type, 'year': year, 'transmission': transmission, 'engine': engine})
            counter += 1
            if counter >= count_cars:
                break
        if counter >= count_cars:
            break
        next_page_button = driver.find_elements(By.XPATH, ("//div[@class='next-page-inner']"))
        if not next_page_button:
            break
        else:
            next_page_button[0].click()
            time.sleep(3)

    print("Number of cars scraped: ", len(cars))
    print("Cars list: ", cars)
    return cars

def write_to_csv(cars):
    with open('cars.csv', mode='w', newline='') as csv_file:
        fieldnames = ['title', 'price', 'liter', 'fuel_type', 'year', 'transmission', 'engine']
        wrt = csv.DictWriter(csv_file, fieldnames=fieldnames)
        wrt.writeheader()

        for car in cars:
            car['title'] = car['title'].strip()
            car['price'] = car['price'].strip()
            wrt.writerow(car)

url = "https://autogidas.lt/en/skelbimai/automobiliai/porsche/"
count_cars = 40
cars = get_cars(url)
write_to_csv(cars)