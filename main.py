from zillow_scraper import Zillow_Soup

zillow_soup = Zillow_Soup()
zillow_soup.scrape_rentals()
print(zillow_soup.rentals_list)

