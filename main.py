from zillow_scraper import Zillow_Soup
from google_forms_filler import Google_Forms_Filler
import time


# scraping "Zillow" website and preparing the soup
zillow_soup = Zillow_Soup()
time.sleep(25)

# creating the rentals list
zillow_soup.scrape_rentals()

# creating the rentals dictionary that contains each rental price, address and its link
zillow_soup.generate_rentals_dict()
print(zillow_soup.rentals_dict)


# creating a Google form filler object
google_forms_filler = Google_Forms_Filler()

# looping through the zillow soup rentals dict and submitting its ifo into the form
for rental in zillow_soup.rentals_dict:
    property_address = zillow_soup.rentals_dict[rental]["rental address"]
    property_price = zillow_soup.rentals_dict[rental]["rental price"]
    property_link = zillow_soup.rentals_dict[rental]["rental link"]
    google_forms_filler.fill_form(property_address, property_price, property_link)
google_forms_filler.driver.quit()
