from selenium import webdriver
from bs4 import BeautifulSoup
import lxml


ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A" \
             "-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C" \
             "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
             "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
             "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D" \
             "%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min" \
             "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"


class Zillow_Soup:
    def __init__(self):
        """This class scrapes 'Zillow' website using selenium webdriver (to ensure that the page has fully loaded
        before scraping it) and the beautiful soup module."""
        self.driver = None
        self.soup = None
        self.scrape()

        self.rentals_list = []
        self.rentals_dict = {}

    def scrape(self):
        """This method scrapes 'Zillow' website and prepares the zillow soup"""
        self.driver = webdriver.Chrome()
        self.driver.get(ZILLOW_URL)

        # waiting for the page to fully load
        self.driver.implicitly_wait(10)

        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')

    def scrape_rentals(self):
        """This method uses the beautiful soup module to get a list of the first page rentals that match the
        specified filters."""
        self.rentals_list = self.soup.select(selector=".List-c11n-8-85-1__sc-1smrmqp-0 "
                                                      ".ListItem-c11n-8-85-1__sc-10e22w8-0")

    def get_rentals_prices(self):
        """This method gets every rental price and adds it to the corresponding rental in the rentals' dictionary
        and deletes the ads from the rentals list."""

        # a variable that acts as an index
        n = 0

        # a list that contains the indexes of the ads to delete them after finding them
        ads_indexes = []
        for rental in self.rentals_list:
            rental_price = 0

            try:
                price = rental.find('span', attrs={'data-test': 'property-card-price'}).get_text()
            except AttributeError:
                # this is an ad
                ads_indexes.append(self.rentals_list.index(rental))
            else:
                if "+" in price:
                    rental_price = price.split("+")[0]
                elif "/" in price:
                    rental_price = price.split("/")[0]

                self.rentals_dict[n] = {
                    "rental price": rental_price,
                }
                n += 1

        # deleting the ads from the rentals list
        for index in ads_indexes:
            del self.rentals_list[index - ads_indexes.index(index)]

    def get_rentals_addresses(self):
        """This method gets every rental address and adds it to the corresponding rental in the rentals' dictionary."""

        # a variable that acts as an index
        n = 0
        for rental in self.rentals_list:
            rental_address = rental.find('address', attrs={'data-test': 'property-card-addr'}).get_text()
            rental_dict = self.rentals_dict[n]
            rental_dict["rental_address"] = rental_address
            n += 1

    def get_rentals_links(self):
        """This method gets every rental link and adds it to the corresponding rental in the rentals' dictionary."""

        # a variable that acts as an index
        n = 0
        for rental in self.rentals_list:
            link = rental.find('a', attrs={'data-test': 'property-card-link'})
            rental_link = link["href"]
            if "https://www.zillow.com" not in rental_link:
                rental_link = "https://www.zillow.com" + rental_link
            rental_dict = self.rentals_dict[n]
            rental_dict["rental_link"] = rental_link
            n += 1

    def generate_rentals_dict(self):
        """This method generates the rentals dictionary that contains each rental price, address and its link."""
        self.get_rentals_prices()
        self.get_rentals_addresses()
        self.get_rentals_links()
