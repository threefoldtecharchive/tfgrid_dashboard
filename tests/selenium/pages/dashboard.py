from selenium.webdriver.common.by import By
from tests.selenium.utils.base import Base

"""
This module contains Dashboard page elements.
"""

class DashboardPage:

    polka_connection_btn = (By.XPATH ,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/button/span/button')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
    
    def polka_connection(self):
        self.browser.find_element(*self.polka_connection_btn).click()

        