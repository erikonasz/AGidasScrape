### Autogidas car scraper.

- This script uses Selenium and BeautifulSoup to scrape car listings from a website, filters out listings for electric cars, and saves the remaining car listings to a CSV file.
- The script navigates to a given URL, accepts cookies, scrapes information about each car on the page, and then proceeds to the next page until a specified number of cars have been scraped or there are no more pages to scrape. 
- The script also extracts specific information about each car, such as its **name[model], price, engine liter, year, fuel type and transmission** and stores this information in a dictionary before writing it to a CSV file.


### How to use it

At the bottom of the code, in the **main()** function
'''Python
def main():
    url = "Your AutoGidas url with cars list. Example - https://autogidas.lt/en/skelbimai/automobiliai/bmw/"
    count_cars = The number of cars to scrape.
'''
As soon as the code is launched, the scraper will scrape the cars list and create a new file called **cars.csv** that contains your scraped car information.
