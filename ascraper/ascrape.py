import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import json
import csv

non_latin_char = re.compile(r"[^\x00-\x7F]+")


def get_cars(url, count_cars):
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(4)
    accept_cookies = driver.find_element(By.XPATH, '//button[text()="I Accept"]')
    accept_cookies.click()
    time.sleep(3)

    cars = []
    counter = 0
    electricity_cars_count = 0

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        allcars = soup.find_all("article", class_="list-item")

        for car in allcars:
            title = car.find("h2", class_="item-title").text
            price = re.sub("[^0-9]", "", car.find("div", class_="item-price").text)
            description = car.find("div", class_="item-description").text
            if "Electricity" in description:
                electricity_cars_count += 1
                continue
            description_list = list(
                filter(
                    None, map(str.strip, "".join(description.splitlines()).split(","))
                )
            )

            if len(description_list) >= 5:
                liter = description_list[0].strip()[:3]
                if len(liter) > 3:
                    liter = "N/A"

                fuel_type = description_list[1].strip()
                if len(fuel_type) > 12:
                    fuel_type = "N/A"

                year = description_list[2].strip()[:4]
                if len(year) > 7:
                    year = "N/A"

                transmission = description_list[3].strip()[:10]
                transmission = re.sub(r"(Automatic.*)", r"Automatic", transmission)
                if len(transmission) > 10:
                    transmission = "N/A"
                city = description_list[-1].strip()

            else:
                liter = "N/A"
                fuel_type = "N/A"
                year = "N/A"
                transmission = "N/A"
                city = "N/A"

            if (
                non_latin_char.search(title)
                or non_latin_char.search(price)
                or non_latin_char.search(liter)
                or non_latin_char.search(fuel_type)
                or non_latin_char.search(year)
                or non_latin_char.search(transmission)
                or non_latin_char.search(city)
            ):
                continue

            cars.append(
                {
                    "title": title,
                    "price": price,
                    "liter": liter,
                    "fuel_type": fuel_type,
                    "year": year,
                    "transmission": transmission,
                    "city": city,
                }
            )
            counter += 1
            if counter >= count_cars:
                break
        if counter >= count_cars:
            break
        next_page_button = driver.find_elements(
            By.XPATH, ("//div[@class='next-page-inner']")
        )
        if not next_page_button:
            break
        else:
            next_page_button[0].click()
            time.sleep(3)

    print("Cars scraped: ", len(cars))
    print("Skipped electric cars:  ", electricity_cars_count)
    print("Caars list: ", cars)
    return cars

def write_to_csv(cars, chunk_size=1000):
    with open("cars.csv", "w", newline="", encoding="utf-8-sig") as csv_file:
        fieldnames = [
            "title",
            "price",
            "liter",
            "fuel_type",
            "year",
            "transmission",
            "city",
        ]
        wrt = csv.DictWriter(csv_file, fieldnames=fieldnames)
        wrt.writeheader()
        for i in range(0, len(cars), chunk_size):
            chunk = cars[i : i + chunk_size]
            for car in chunk:
                if not isinstance(car["title"], str) or not isinstance(
                    car["price"], str
                ):
                    continue
                car["title"] = car["title"].strip()
                car["price"] = car["price"].strip()
                wrt.writerow(car)


def main():
    url = "https://autogidas.lt/en/skelbimai/automobiliai/?f_1%5B0%5D=&f_model_14%5B0%5D=&f_215=&f_216=&f_41=&f_42=&f_376="
    count_cars = 10500
    cars = get_cars(url, count_cars)
    write_to_csv(cars)


main()
