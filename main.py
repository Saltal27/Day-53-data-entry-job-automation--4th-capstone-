from zillow_scraper import Zillow_Soup

# scraping "Zillow" website and preparing the soup
zillow_soup = Zillow_Soup()

# creating the rentals list
zillow_soup.scrape_rentals()

# creating the rentals dictionary that contains each rental price, address and its link
zillow_soup.generate_rentals_dict()
print(zillow_soup.rentals_dict)



