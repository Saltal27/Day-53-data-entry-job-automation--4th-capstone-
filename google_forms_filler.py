# import win32api
# from undetected_chromedriver import Chrome
# from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time

# win32api.SetConsoleCtrlHandler(lambda x: True)
# driver path
chrome_driver_path = r"C:\Development\chromedriver.exe"


class Google_Forms_Filler:
    def __init__(self):
        self.driver = None
        self.create_driver()

    def create_driver(self):
        """This method creates a driver and navigates to the form."""
        # options = Options()
        # options.add_argument("--lang=en")
        # self.driver = Chrome(options=options)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        service = Service(executable_path=chrome_driver_path)
        self.driver = WebDriver(service=service, options=options)
        self.driver.maximize_window()
        self.driver.get(
            "https://docs.google.com/forms/d/e/1FAIpQLScV3nfgqtdTn42qRUfvZGFhLhXfRa-XAyo8MWkiqIhMEfSoBQ/viewform")
        time.sleep(5)

    def fill_form(self, property_address, property_price, property_link):
        """This method refreshes the page and fills in a new form with different info."""
        self.driver.get(
            "https://docs.google.com/forms/d/e/1FAIpQLScV3nfgqtdTn42qRUfvZGFhLhXfRa-XAyo8MWkiqIhMEfSoBQ/viewform")
        time.sleep(5)

        address = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                     '2]/div/div[1]/div/div[1]/input')
        address.send_keys(property_address)

        price = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                   '2]/div/div[1]/div/div[1]/input')
        price.send_keys(property_price)

        link = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]'
                                                  '/div/div[1]/div/div[1]/input')
        link.send_keys(property_link)

        submit = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
        submit.click()
